from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

DB = 'database.db'

# ------------------- Initialize Database -------------------
def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    # Users table
    c.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT)''')
    # Posts table
    c.execute('''CREATE TABLE IF NOT EXISTS posts (id INTEGER PRIMARY KEY, title TEXT, content TEXT)''')
    # Default admin user
    c.execute("INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)",
              ("admin", generate_password_hash("admin123")))
    conn.commit()
    conn.close()

init_db()

# ------------------- Routes -------------------

# Home page
@app.route('/')
def index():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT id, title, content FROM posts ORDER BY id DESC")
    posts = c.fetchall()
    conn.close()
    return render_template('index.html', posts=posts)

# Blog listing page
@app.route('/blog')
def blog():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT id, title, content FROM posts ORDER BY id DESC")
    posts = c.fetchall()
    conn.close()
    return render_template('blog.html', posts=posts)

# Projects page
@app.route('/projects')
def projects():
    projects_list = [
        {'name': 'AGI Module', 'link': '#'},
        {'name': 'Python Automation', 'link': '#'},
        {'name': 'Web Scraper', 'link': '#'}
    ]
    return render_template('project.html', projects=projects_list)

# Business Experiments
@app.route('/business')
def business():
    experiments_list = [
        {'name': 'Meesho Reselling', 'link': '#'},
        {'name': 'Electronics Shop', 'link': '#'}
    ]
    return render_template('business.html', experiments=experiments_list)

# About Me
@app.route('/about')
def about():
    return render_template('about.html')

# Contact / Newsletter Signup
@app.route('/contact', methods=['GET','POST'])
def contact():
    if request.method == 'POST':
        email = request.form['email']
        print(f"New subscriber: {email}")  # Future: Save to DB / send email
        return "Thank you for subscribing!"
    return render_template('contact.html')

# ------------------- Admin Routes -------------------

# Admin login
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect(DB)
        c = conn.cursor()
        c.execute("SELECT password FROM users WHERE username=?", (username,))
        user = c.fetchone()
        conn.close()
        if user and check_password_hash(user[0], password):
            session['admin'] = username
            return redirect(url_for('admin_dashboard'))
        else:
            return "Invalid credentials"
    return render_template('admin_login.html')

# Admin dashboard
@app.route('/admin/dashboard')
def admin_dashboard():
    if 'admin' not in session:
        return redirect(url_for('admin_login'))
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT id, title FROM posts ORDER BY id DESC")
    posts = c.fetchall()
    conn.close()
    return render_template('admin_dashboard.html', posts=posts)

# Add new post
@app.route('/admin/add', methods=['GET', 'POST'])
def add_post():
    if 'admin' not in session:
        return redirect(url_for('admin_login'))
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        conn = sqlite3.connect(DB)
        c = conn.cursor()
        c.execute("INSERT INTO posts (title, content) VALUES (?, ?)", (title, content))
        conn.commit()
        conn.close()
        return redirect(url_for('admin_dashboard'))
    return render_template('add_post.html')

# Logout
@app.route('/admin/logout')
def admin_logout():
    session.pop('admin', None)
    return redirect(url_for('index'))

# ------------------- Run App -------------------
if __name__ == '__main__':
    app.run(debug=True)
