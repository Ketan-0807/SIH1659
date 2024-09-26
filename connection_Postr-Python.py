import psycopg2

# Define the database connection parameters
host = 'localhost'
database = 'ddas'
username = 'postgres'
password = 'QWER123!@#'

# Establish a connection to the database
conn = psycopg2.connect(
    host=host,
    database=database,
    user=username,
    password=password
)

# Create a cursor object
cur = conn.cursor()

# Execute a query to test the connection
cur.execute("SELECT version()")

# Fetch the result
db_version = cur.fetchone()

# Print the result
print(db_version)

# Close the cursor and connection
cur.close()
conn.close()