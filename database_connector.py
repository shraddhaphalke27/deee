import mysql.connector
from mysql.connector import Error
def execute_sql_query(query):
    print("Executing query:", query)
    # Define your database connection parameters
    conn = None
    cursor = None
 
    try:
        # Establish the database connection
        conn = mysql.connector.connect(
            user='root',
            password='root',
            host='localhost',
            database='commandcenterdb_dev'
        )
        # Check if the connection is successful
        if conn.is_connected():
            print("Database connected successfully!")
        else:
            print("Failed to connect to the database.")
            return [], []
 
        # Create a cursor object
        cursor = conn.cursor()
 
        # Execute the query
        cursor.execute(query)
 
        # Fetch the results
        results = cursor.fetchall()
        print(results)
 
        # Get the column names
        column_names = [i[0] for i in cursor.description]
 
        return column_names, results
 
    except mysql.connector.Error as err:
        # Handle MySQL-specific errors
        print(f"MySQL Error: {err}")
        return [], []
    except Exception as e:
        # Handle other general errors
        print(f"An unexpected error occurred: {e}")
        return [], []
    finally:
        # Ensure that the cursor and connection are closed properly
        if cursor:
            cursor.close()
            print("Cursor closed.")
        if conn and conn.is_connected():
            conn.close()
            print("Database connection closed.")
