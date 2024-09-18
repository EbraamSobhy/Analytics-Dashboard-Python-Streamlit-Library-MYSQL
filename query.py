import os
import mysql.connector
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

def get_connection():
    """
    Establish a connection to the MySQL database using environment variables.
    """
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

def view_all_data():
    """
    Fetch all data from the `python_query_csv` table.
    """
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM python_query_csv')
        data = cursor.fetchall()
        return data
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return []
    finally:
        conn.close()
