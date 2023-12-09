import mysql.connector, datetime

connection = mysql.connector.connect(host="localhost",
                                     port="3306",
                                     database="summarizer",
                                     user="root",
                                     password="Gisprog_1")

def main():
    cursor = connection.cursor()

    selectQuery = "SELECT * FROM USER"

    cursor.execute(selectQuery)
    rows=cursor.fetchall()

    print(f"Number of rows retrieved from user table: {cursor.rowcount}")
    print()

    for row in rows:
        print(f"user_id:    {row[0]}")
        print(f"username:   {row[1]}")
        print(f"password:   {row[2]}")
        print()

##    selectQuery = \
##    "SELECT * FROM summary JOIN user ON summary.user_id = user.user_id \
##    WHERE user.user_id = 1"

    selectQuery = "SELECT * FROM SUMMARY"

    cursor.execute(selectQuery)
    rows=cursor.fetchall()

    print(f"Number of rows retrieved from summary table: {cursor.rowcount}")
    print()

    for row in rows:
        print(f"summary_id:     {row[0]}")
        print(f"created_date:   {row[1]}")
        print(f"article_text:   {row[2]}")
        print(f"article_url:    {row[3]}")
        print(f"summary_text:   {row[4]}")
        print(f"summary_length: {row[5]}")
        print(f"user_id: {row[6]}")
        print()

    created_date = "2023-12-06"
    article_text = "Here is some sample article text."
    article_url = None
    summary_text = "And a summary as well."
    summary_length = None
    user_id = 7

    value_list = []
    value_list.append(created_date)
    value_list.append(article_text)
    value_list.append(article_url)
    value_list.append(summary_text)
    value_list.append(summary_length)
    value_list.append(user_id)
    
    selectQuery = f"INSERT INTO summary (created_date, article_text, article_url, summary_text, summary_length, user_id) VALUES (%s, %s, %s, %s, %s, %s)"

    cursor.execute(selectQuery, value_list)
    connection.commit()

    cursor.close()
    connection.close()

if __name__ == "__main__":
    main()
