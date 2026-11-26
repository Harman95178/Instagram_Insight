
import pandas as pd
from db_connection import create_connection

# Connect to MySQL
conn = create_connection()

if conn:
    try:
        # Fetch Instagram data
        query = "SELECT * FROM instagram_posts"

        df = pd.read_sql(query, conn)

        # Display results
        print("\nData fetched successfully!")
        print("Total rows and columns:", df.shape)

        print("\nFirst 5 records:")
        print(df.head())

        print("\nColumn names:")
        print(df.columns.tolist())

    finally:
        conn.close()
        print("\nMySQL connection closed.")
