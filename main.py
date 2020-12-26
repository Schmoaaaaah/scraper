import os

import mysql
from instagrapi import Client
from mysql.connector import Error
from dotenv import load_dotenv

def main():
    load_dotenv()
    insta_user = os.getenv('INSTA_USER')
    print(insta_user)
    insta_pas = os.getenv('INSTA_PAS')
    insta = Client()
    insta.login(insta_user, insta_pas)
    userid = insta.user_id_from_username(insta_user)
    connection = create_server_connection()
    saveposts(insta, userid, connection)
    saveprofile(insta, userid, connection)


def saveposts(insta, userid, connection):
    posts = insta.user_medias(userid)
    for post in posts:
        print('Media with ID: ' + str(post.dict()) + 'found. JSON: ' + str(post))
        query = ''
        execute_query(connection, query)


def saveprofile(insta, userid, connection):
    user = insta.user_info(userid)
    print('Profile from user: ' + str(user.dict()) + ' JSON: ' + str(user))
    query = ''
    execute_query(connection,query)

def create_server_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            passwd=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection

def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")


main()
