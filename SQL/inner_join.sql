USE summarizer;

SELECT summary_id, created_date, article_text, article_url, summary_text, summary.user_id
FROM summary JOIN user
	ON summary.user_id = user.user_id
WHERE user.user_id = 1;
