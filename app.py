from flask import Flask, request, render_template, redirect, url_for, flash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Setup SQLite database
def init_db():
    if not os.path.exists('simple.db'):
        conn = sqlite3.connect('simple.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)''')
        c.execute('INSERT INTO users (username, password) VALUES (?, ?)', ('admin', 'password'))
        conn.commit()
        conn.close()

init_db()

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    conn = sqlite3.connect('simple.db')
    c = conn.cursor()
    
    # Vulnerable query
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    c.execute(query)

    #Parametrized Query for protection
    # query = "SELECT * FROM users WHERE username = ? AND password = ?"
    # c.execute(query, (username, password))
    
    user = c.fetchone()
    conn.close()
    
    if user:
        flash('Login successful!', 'success')
        return redirect(url_for('index'))
    else:
        flash('Login failed! Please check your username and password.', 'danger')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
