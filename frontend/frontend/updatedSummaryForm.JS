import "./App.css";
import { useState } from "react";
import axios from "axios";
import { RemoteRunnable } from "langchain/runnables/remote";

function SummaryForm(props) {
    console.log("In SummaryForm");
    console.log(`props: ${props.userName}`);
    console.log(`props: ${props.userData}`);
    //console.log(`props: ${props.userData[0]["created_date"]}`);
    const [createdDate, setCreatedDate] = useState(props.userData[0]["created_date"]);
    const [article, setArticle] = useState(props.userData[0]["article_text"]);
    const [articleURL, setArticleURL] = useState(props.userData[0]["article_url"]);
    const [summary, setSummary] = useState(props.userData[0]["summary_text"]);
    const [summaryLength, setSummaryLength] = useState(props.userData[0]["summary_length"]);
    const [summaryIndex, setSummaryIndex] = useState(0);
    //const [errorMessage, setErrorMessage] = useState("");

    const handleInputChange = (setInput, event) => {
        setInput(event.target.value);
        console.log("Handled input change");
    };

    const setStateVars = (arrayIndex) => {
        setCreatedDate(props.userData[arrayIndex]["created_date"]);
        setArticle(props.userData[arrayIndex]["article_text"]);
        setArticleURL(props.userData[arrayIndex]["article_url"]);
        setSummary(props.userData[arrayIndex]["summary_text"]);
        setSummaryLength(props.userData[arrayIndex]["summary_length"]);
        setSummaryIndex(arrayIndex);
    }

    const handleFirstClicked= () => {
        setStateVars(0);
    };

    const handlePrevClicked= () => {
        if ((summaryIndex - 1) >= 0) {
            setStateVars(summaryIndex - 1);
        }
    };

    const handleNextClicked= () => {
        if ((summaryIndex + 1) < props.userData.length) {
            setStateVars(summaryIndex + 1);
        }
    };

    const handleLastClicked= () => {
        setStateVars(props.userData.length -1);
    };

    const handleAddNewClicked = () => {
        // Retrieve current date and format as required.
        const date = new Date();
        console.log(`Date: ${date}`);
        console.log(`Day: ${date.getDay()}`);
        const formatedDate = `${date.getFullYear()}-${date.getMonth()+1}-${date.getDate()}`;
        setCreatedDate(formatedDate);
        setArticle("");
        setArticleURL("");
        setSummary("");
        setSummaryLength(0);
    }

    const handleSummarizeClicked = async (event) => {
        if (article == "" && articleURL == "") {
            alert("One of Article or Article URL must be specified.");
        } else if (summaryLength == 0) {
            alert("A non-zero summary length must be supplied.");
        } else if (article != "") {
            const summary_chain = new RemoteRunnable({url: `http://127.0.0.1:8000/summary_chain/`,});
            const result = await summary_chain.invoke({"article_text":article, "summary_length":summaryLength,});
            console.log(result);
        } else {
            const url_summary_chain = new RemoteRunnable({url:`http://127.0.0.1:8000/url_summary_chain/`,});
            const result = await url_summary_chain.invoke({"article_text":article, "summary_length":summaryLength});
            console.log(result);
        }
    }

    const handleSubmitClicked = (event) => {
        // Validate form fields prior to post.
        if ((createdDate == "") ||
            (article == "" && articleURL == "") ||
            (summary == "") ||
            (summaryLength == 0)) {
            alert("One or more field values are invalid.");
        } else {
            // If both an article and a url are specified, retain the
            // article text only.
            if (article != "") {
                setArticleURL("");
            }
            axios
                .post(`http://127.0.0.1:5000/add_new/${props.userName}`,
                    {"created_date": createdDate,
                    "article_text":article,
                    "article_url":articleURL,
                    "summary_text":summary,
                    "summary_length":summaryLength})
                .then ((res) => {console.log(res.data);});
        }
        event.preventDefault();
    }

    return (
        <form className="summary" name="summaryForm">
            <label htmlFor="article">Article:</label>
            <textarea
                className="article"
                id="article"
                name="article"
                placeholder="Please enter article here"
                value={article}
                onChange={(e) => handleInputChange(setArticle, e)}
            />
            <br/>
            <label htmlFor="summary">Summary:</label>
            <textarea
                className="summary"
                id="summary"
                name="summary"
                value={summary}
                onChange={(e) => handleInputChange(setSummary, e)}
                disabled
            />
            <br/>
            <label htmlFor="articleURL">Article URL:</label>
            <input
                type="text"
                className="inputfield"
                id="articleURL"
                name="articleURL"
                placeholder="Enter url as article source"
                size="75"
                value={articleURL}
                onChange={(e) => handleInputChange(setArticleURL, e)}
            />
            <br/>
            <label htmlFor="summarylength">Summary Length:</label>
            <input
                type="text"
                className="inputfield"
                id="summarylength"
                name="summarylength"
                size="10"
                value={summaryLength}
                onChange={(e) => handleInputChange(setSummaryLength, e)}
            />
            <p>Showing <span id="current">{summaryIndex + 1}</span> of <span id="total">{props.userData.length}</span>     Date Created: <span id="date">{createdDate}</span></p>
            <br/>
            <input
                type="button"
                className="formButton"
                id="first"
                name="first"
                value="First"
                onClick={handleFirstClicked}
            />
            <input
                type="button"
                className="formButton"
                id="prev"
                name="prev"
                value="Prev"
                onClick={handlePrevClicked}
            />
            <input
                type="button"
                className="formButton"
                id="next"
                name="next"
                value="Next"
                onClick={handleNextClicked}
            />
             <input
                type="button"
                className="formButton"
                id="last"
                name="last"
                value="Last"
                onClick={handleLastClicked}
            />
            <input
                type="button"
                className="formButton"
                id="add"
                name="add"
                value="Add New"
                onClick={handleAddNewClicked}
            />
            <input
                type="submit"
                className="formButton"
                id="submit"
                name="submit"
                value="Submit"
                onClick={(e) => handleSubmitClicked(e)}
            />
            <input
                type="reset"
                className="formButton"
                id="Summarize"
                name="Summarize"
                value="Summarize"
                onClick={(e) => handleSummarizeClicked(e)}
            />
        </form>
    )
}

export default SummaryForm;
