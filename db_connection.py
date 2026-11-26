
import mysql.connector

def create_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="blessyouharman8102004",
            database="instagram_analytics"
        )

        if connection.is_connected():
            print("MySQL Connected Successfully!")
            return connection

    except mysql.connector.Error as error:
        print("Connection Error:", error)
        return None


# Test database connection
conn = create_connection()

if conn:
    conn.close()
    print("Connection Closed Successfully!")
