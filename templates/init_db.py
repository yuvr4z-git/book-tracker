import pymssql

# Extract the details from your Azure connection string:
server = 'book-server-uv.database.windows.net'
user = 'yuvr4z'
password = 'Yuvi@2211'
database = 'book-db'

print("Connecting to Azure SQL Database via pure-Python driver...")
try:
    conn = pymssql.connect(server, user, password, database)
    cursor = conn.cursor()

    print("Creating 'books' table...")
    # SQL query to create table if it doesn't exist
    cursor.execute('''
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='books' AND xtype='U')
        CREATE TABLE books (
            id INT IDENTITY(1,1) PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            author VARCHAR(255) NOT NULL,
            status VARCHAR(50) NOT NULL,
            rating INT NULL
        )
    ''')

    cursor.execute('''
                   INSERT INTO books (title, author, status, rating)
                   VALUES ('The Alchemist', 'Paulo Coelho', 'Reading', 5)
                   ''')

    conn.commit()
    print("🎉 Database initialized successfully with starter data!")

    cursor.close()
    conn.close()

except Exception as e:
    print(f"❌ Error connecting: {e}")