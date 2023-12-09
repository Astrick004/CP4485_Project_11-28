# Program:  LLM_server.py
# Author:   Andrew Strickland
# Date:     2023-12-07
# Purpose:  LLM server component of the Article Summarizer app - utilizes LangServ.

from fastapi import FastAPI
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate, StringPromptTemplate
from langchain.schema import BaseOutputParser
from pydantic import BaseModel, validator
import requests
from newspaper import Article
from langserve import add_routes


class BareStringOutputParser(BaseOutputParser[str]):
    """Parse the output of a LLM call to remove leading and trailing white space."""

    def parse(self, text: str) -> str:
        """Parse the output of an LLM call."""
        return text.strip("\n ")


def scrape_article_url(article_url):
    """Scrape an article url to retrieve text content only."""

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
    }

    session = requests.Session()

    try:
        response = session.get(article_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            article = Article(article_url)
            article.download()
            article.parse()
            return article.text
        else:
            print(f"Failed to fetch article at {article_url}")
    except Exception as e:
        print(f"Error occurred while fetching article at {article_url}: {e}")


template = """You are a very good assistant that writes coherent, concise article summaries.

Here's the article you want to summarize.

{article_text}

Summarize the previous article in at most {summary_length} words.
"""


class ArticleURLPromptTemplate(StringPromptTemplate):
    """A custom prompt template that provides for initial scraping of an article identified by URL."""

    def format(self, **kwargs) -> str:
        # Scrap the article url to retrieve the text content.
        article_text = scrape_article_url(kwargs["article_url"])

        # Generate the prompt to be sent to the language model
        prompt = template.format(
            article_text=article_text, summary_length=kwargs["summary_length"]
        )
        return prompt

    def _prompt_type(self):
        return "article url scraper"


# Instantiate an article url prompt template.
scraper = ArticleURLPromptTemplate(input_variables=["article_url","summary_length"])

# Instantiate a text article prompt template.
prompt_template = PromptTemplate.from_template(template)

# Simple llm model specification.
llm = OpenAI(openai_api_key="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", temperature=0)

# Define the chains to expose via the api.
url_summary_chain = scraper | llm | BareStringOutputParser()

summary_chain = prompt_template | llm | BareStringOutputParser()

#summary = chain.invoke({"article_text":article.text, "summary_length":"75"})
#summary = chain.invoke({"article_url":"https://www.cbc.ca/news/politics/liberal-government-unveils-oil-gas-cap-1.7051803", "summary_length":"50"})

app = FastAPI(
    title="LangChain Server",
    version="1.0",
    description="A simple API server for the Article Summarizer app",
)

# Route for articles based on a url.
add_routes(
    app,
    url_summary_chain,
    path="/url_summary_chain",
)

# Route for articles supplied as text at the outset.
add_routes(
    app,
    summary_chain,
    path="/summary_chain",
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
