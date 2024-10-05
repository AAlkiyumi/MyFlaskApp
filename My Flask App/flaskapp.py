from flask import Flask, render_template, request, redirect, url_for, flash, send_file
import sqlite3

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Needed for flashing messages

# SQLite setup
def get_db_connection():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row  # Allows dictionary-like access to rows
    return conn

# Home route, redirects to register page
@app.route('/')
def index():
    return redirect(url_for('register'))

# Register route to render the registration form
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']

        conn = get_db_connection()
        c = conn.cursor()
        c.execute("INSERT INTO users (username, password, firstname, lastname, email) VALUES (?, ?, ?, ?, ?)",
                  (username, password, firstname, lastname, email))
        conn.commit()
        conn.close()

        return redirect(url_for('profile', username=username))
    return render_template('register.html')

# Login route for returning users
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = c.fetchone()
        conn.close()

        if user:
            return redirect(url_for('profile', username=username))
        else:
            flash('Invalid username or password. Please try again.')

    return render_template('login.html')

# Profile route to display user information
@app.route('/profile/<username>')
def profile(username):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    user = c.fetchone()
    conn.close()

    if user:
        return render_template('profile.html', user=user)
    else:
        return 'User not found', 404

# Extra credit: Upload and word count
@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    file.save('Limerick-1.txt')

    with open('Limerick-1.txt', 'r') as f:
        text = f.read()
        word_count = len(text.split())

    return f"File uploaded successfully! Word count: {word_count}"

@app.route('/download')
def download():
    return send_file('Limerick-1.txt', as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)


