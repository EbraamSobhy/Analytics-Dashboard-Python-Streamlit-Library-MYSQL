import mysql.connector
import streamlit as st

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
