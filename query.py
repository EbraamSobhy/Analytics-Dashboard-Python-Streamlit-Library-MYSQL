import os
import mysql.connector
import streamlit as st
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from a .env file

# Connection
conn = mysql.connector.connect(
    host="localhost",
    port="3306",
    user="root",
    passwd = "Sy5gGg3UJomPeF",
    database="my_db"
)

c = conn.cursor()

# Fetch data from database
def view_all_data():
    c.execute('SELECT * FROM python_query_csv')
    data = c.fetchall()
    return data


def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )
