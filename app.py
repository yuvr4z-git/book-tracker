import os
from flask import Flask, render_template, request, redirect, url_for, flash
import pymssql

app = Flask(__name__)
# Secure fallback for secret key needed for flash messages
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'dev_secret_key_12345')

# Database Configuration Configuration Slots
DB_SERVER = 'book-tracker-rg.database.windows.net'
DB_USER = 'yuvr4z@book-tracker-rg'
DB_PASSWORD = 'Yuvi@2211'
DB_NAME = 'book-db'


def get_db_connection():
    """Establishes a secure connection to the Azure SQL Database with strict parameters."""
    try:
        conn = pymssql.connect(
            server=DB_SERVER,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            port=1433,              # Explicit port assignment
            tds_version='7.3',     # Forces modern SQL Server protocol translation
            conn_properties='SET ANSI_NULLS ON; SET ANSI_WARNINGS ON;', # Standard protocol compliance
            timeout=30
        )
        return conn
    except Exception as e:
        print(f"❌ DATABASE CONNECTION ERROR: {e}")
        return None


@app.route('/')
def index():
    conn = get_db_connection()
    if not conn:
        return "Database Connection Failed. Check server logs and firewall rules.", 500

    try:
        cursor = conn.cursor(as_dict=True)
        cursor.execute("SELECT id, title, author, status, rating FROM books ORDER BY id DESC")
        books = cursor.fetchall()
        return render_template('index.html', books=books)
    except Exception as e:
        print(f"❌ Query Execution Failed: {e}")
        return f"Error loading library data: {e}", 500
    finally:
        conn.close()


@app.route('/add', methods=['POST'])
def add_book():
    title = request.form.get('title')
    author = request.form.get('author')
    status = request.form.get('status', 'Want to Read')
    rating = request.form.get('rating')

    # Convert empty string to None for integer column parsing
    rating = int(rating) if rating and rating.isdigit() else None

    if not title or not author:
        flash("Title and Author fields are required!", "danger")
        return redirect(url_for('index'))

    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO books (title, author, status, rating) VALUES (%s, %s, %s, %s)",
                (title, author, status, rating)
            )
            conn.commit()
            flash("Book added to tracking array successfully!", "success")
        except Exception as e:
            print(f"❌ Insert Failed: {e}")
            flash(f"Error adding record: {e}", "danger")
        finally:
            conn.close()
    else:
        flash("Database unavailable. Action canceled.", "danger")

    return redirect(url_for('index'))


@app.route('/delete/<int:book_id>', methods=['POST'])
def delete_book(book_id):
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM books WHERE id = %s", (book_id,))
            conn.commit()
            flash("Book removed cleanly.", "info")
        except Exception as e:
            print(f"❌ Delete Failed: {e}")
            flash(f"Error removing record: {e}", "danger")
        finally:
            conn.close()
    return redirect(url_for('index'))


if __name__ == '__main__':
    # Local development server initialization
    app.run(debug=True, host='0.0.0.0', port=5000)