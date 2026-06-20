from flask import Flask, render_template, request, redirect, url_for
import pymssql
import pyodbc

app = Flask(__name__)

# 🛠️ Database Connection Details (Replace with your info!)
DB_SERVER = 'book-server-uv.database.windows.net'
DB_USER = 'yuvr4z'
DB_PASSWORD = 'Yuvi@2211'
DB_NAME = 'book-db'


def get_db_connection():
    # Helper function to open a connection to Azure SQL
    return pymssql.connect(DB_SERVER, DB_USER, DB_PASSWORD, DB_NAME)


@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor(as_dict=True)  # as_dict=True makes rows behave like Python dicts

    # Fetch all books from the Azure SQL Database
    cursor.execute('SELECT id, title, author, status, rating FROM books')
    cloud_books = cursor.fetchall()

    cursor.close()
    conn.close()

    # Send the live data to your index.html file
    return render_template('index.html', books=cloud_books)


@app.route('/add', methods=['POST'])
def add_book():
    title = request.form.get('title')
    author = request.form.get('author')
    status = request.form.get('status')

    if title and author:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Insert the user's form input straight into the cloud table
        cursor.execute(
            "INSERT INTO books (title, author, status, rating) VALUES (%s, %s, %s, NULL)",
            (title, author, status)
        )

        conn.commit()
        cursor.close()
        conn.close()

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)

# Replace your old connection line with this:
conn_str = (
    "Driver={ODBC Driver 18 for SQL Server};"
    "Server=tcp:YOUR_SERVER_NAME.database.windows.net,1433;"
    "Database=YOUR_DATABASE_NAME;"
    "Uid=YOUR_USERNAME;"
    "Pwd=YOUR_PASSWORD;"
    "Encrypt=yes;"
    "TrustServerCertificate=no;"
    "Connection Timeout=30;"
)
conn = pyodbc.connect(conn_str)