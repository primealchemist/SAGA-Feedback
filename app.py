from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from apscheduler.schedulers.background import BackgroundScheduler
import atexit
import datetime
import logging

app = Flask(__name__, static_folder='static')

logging.getLogger('apscheduler.util').addFilter(lambda record: not record.getMessage().startswith('The localize method'))

def init_db():
    with sqlite3.connect('feedback.db') as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS feedback (
                            id INTEGER PRIMARY KEY AUTOINCREMENT, 
                            name TEXT, 
                            email TEXT, 
                            topic TEXT, 
                            message TEXT,
                            likes INTEGER DEFAULT 0,
                            dislikes INTEGER DEFAULT 0);''')
        conn.execute('''CREATE TABLE IF NOT EXISTS comments (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            post_id INTEGER,
                            comment TEXT,
                            FOREIGN KEY (post_id) REFERENCES feedback (id));''')
        conn.commit()


def reset_db():
    with sqlite3.connect('feedback.db') as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM feedback")
        conn.commit()

def schedule_weekly_reset():
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=reset_db, trigger="interval", weeks=1, start_date="2023-04-08 00:00:00")
    scheduler.start()

    atexit.register(lambda: scheduler.shutdown())

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    email = request.form['email']
    topic = request.form['dropdown']
    message = request.form['message']

    with sqlite3.connect('feedback.db') as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO feedback (name, email, topic, message) VALUES (?, ?, ?, ?)", (name, email, topic, message))
        conn.commit()

    return redirect(url_for('posts'))

@app.route('/reset')
def reset():
    reset_db()
    return redirect(url_for('index'))

@app.route('/posts')
def posts():
    with sqlite3.connect('feedback.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM feedback ORDER BY id DESC")
        all_posts = cursor.fetchall()
        cursor.execute("SELECT * FROM comments")
        all_comments = cursor.fetchall()

    return render_template('posts.html', posts=all_posts, comments=all_comments)
@app.route('/like/<int:post_id>', methods=['POST'])
def like(post_id):
    with sqlite3.connect('feedback.db') as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE feedback SET likes = likes + 1 WHERE id = ?", (post_id,))
        conn.commit()
    return redirect(url_for('posts'))

@app.route('/dislike/<int:post_id>', methods=['POST'])
def dislike(post_id):
    with sqlite3.connect('feedback.db') as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE feedback SET dislikes = dislikes + 1 WHERE id = ?", (post_id,))
        conn.commit()
    return redirect(url_for('posts'))

@app.route('/add_comment/<int:post_id>', methods=['POST'])
def add_comment(post_id):
    comment_text = request.form['comment']
    with sqlite3.connect('feedback.db') as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO comments (post_id, comment) VALUES (?, ?)", (post_id, comment_text))
        conn.commit()
    return redirect(url_for('posts'))
def update_feedback_table():
    with sqlite3.connect('feedback.db') as conn:
        cursor = conn.cursor()
        
        cursor.execute("PRAGMA table_info(feedback);")
        columns = cursor.fetchall()
        column_names = [col[1] for col in columns]

        if 'likes' not in column_names:
            conn.execute('''ALTER TABLE feedback ADD COLUMN likes INTEGER DEFAULT 0;''')
            conn.commit()

        if 'dislikes' not in column_names:
            conn.execute('''ALTER TABLE feedback ADD COLUMN dislikes INTEGER DEFAULT 0;''')
            conn.commit()

        if 'comments' not in column_names:
            conn.execute('''CREATE TABLE IF NOT EXISTS comments (id INTEGER PRIMARY KEY AUTOINCREMENT, post_id INTEGER, content TEXT);''')
            conn.commit()
@app.route('/delete/<int:post_id>', methods=['GET', 'POST'])
def delete_post(post_id):
    with sqlite3.connect('feedback.db') as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM feedback WHERE id=?", (post_id,))
        conn.commit()
    return redirect(url_for('posts'))







if __name__ == '__main__':
    init_db()
    update_feedback_table()
    schedule_weekly_reset()
    app.run(debug=True)

