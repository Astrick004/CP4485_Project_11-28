# Program:  __init__.py
# Author    Andrew Strickland
# Date:     2023-12-01
# Purpose:  Flask back end for the Article Summarizer app.  Facilitates data retrieval
#           and writing to a MySQL database.

from flask import Flask
from markupsafe import escape
import mysql.connector
from datetime import datetime
from flask_cors import CORS
from flask import request

app = Flask(__name__)
CORS(app)  # Avoid cross-origin errors.

@app.route("/")
def index():
    return "<p>Here is the Index page</p>"

# Data retrieval route based on specified username.
@app.route("/data/<username>", methods=["GET"], strict_slashes=False)
def data(username):

    try:
    
        connection = mysql.connector.connect(host="localhost",
                                         port="3306",
                                         database="summarizer",
                                         user="root",
                                         password="Gisprog_1")

        selectQuery = f"SELECT * FROM user WHERE username = '{username}'"

        cursor = connection.cursor()
        cursor.execute(selectQuery)
        row = cursor.fetchone()
        user_id = row[0]
   
        selectQuery = f"SELECT * FROM summary WHERE user_id = {user_id}"

        cursor.execute(selectQuery)
        rows = cursor.fetchall()

        row_list = []

        if cursor.rowcount == 0:
            # Create empty object to ensure returned list has at least one entry.
            row_list.append({"created_date":"", \
                             "article_text":"", \
                             "article_url":"", \
                             "summary_text":"", \
                             "summary_length":0})
        else:
            for row in rows:
                # Check columns that accept null values and set to non-null.
                article_text = row[2]
                if article_text == None:
                    article_text = ""
                article_url = row[3]
                if article_url == None:
                    article_url = ""
                summary_length = row[5]
                if summary_length == None:
                    summary_length = 0
                # Format date column.
                date_string = f"{row[1]:%Y-%m-%d}"
                # Create json format object for current row and append to the list.
                row_list.append({"created_date":date_string, \
                                 "article_text":article_text, \
                                 "article_url":article_url, \
                                 "summary_text":row[4], \
                                 "summary_length":summary_length})

        # Close the database cursor and connection.
        cursor.close()
        connection.close()

        # Return the data for the identified user.
        return {"data":row_list,
                "code":200}

    except Exception as e:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
        return {"error":e.__str__(), "code":404}


# Data addition route based on specified username.
@app.route("/add_new/<username>",methods=["POST"], strict_slashes=False)
def add_new(username):
    try:
    
        new_data = request.get_json()
        
        created_date = new_data["created_date"]
        article_text = new_data["article_text"]
        article_url = new_data["article_url"]
        summary_text = new_data["summary_text"]
        summary_length = new_data["summary_length"]

        connection = mysql.connector.connect(host="localhost",
                 port="3306",
                 database="summarizer",
                 user="root",
                 password="Gisprog_1")

        selectQuery = f"SELECT * FROM user WHERE username = '{username}'"

        cursor = connection.cursor()
        cursor.execute(selectQuery)
        row = cursor.fetchone()
        user_id = row[0]
   
        selectQuery = "INSERT INTO summary (created_date, article_text, article_url, summary_text, summary_length, user_id) VALUES (%s, %s, %s, %s, %s, %s)"

        value_list = []
        value_list.append(created_date)
        value_list.append(article_text)
        value_list.append(article_url)
        value_list.append(summary_text)
        value_list.append(summary_length)
        value_list.append(user_id)

        cursor.execute(selectQuery, value_list)
        connection.commit()

        cursor.close()
        connection.close()

        return {"code":200}
    
    except Exception as e:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
        return {"error":e.__str__(), "code":404}
    

@app.route("/welcome")
def welcome():
    return f"Welcome to my app!"

@app.route("/<name>")
def welcome_name(name):
    return f"Welcome, {escape(name)}!"

if __name__ == "__main__":
    app.run()
