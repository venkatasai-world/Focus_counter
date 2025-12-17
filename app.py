from flask import Flask, render_template, redirect, url_for
import sqlite3
from datetime import date

app = Flask(__name__)

# Create database and table if not exists
def init_db():
    conn = sqlite3.connect("focus.db")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS focus (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT UNIQUE,
            distractions INTEGER
        )
    """)
    conn.commit()
    conn.close()

@app.route('/')
def home():
    conn = sqlite3.connect("focus.db")
    cur = conn.cursor()
    cur.execute("SELECT date, distractions FROM focus ORDER BY date DESC")
    data = cur.fetchall()
    conn.close()
    return render_template("index.html", data=data)

@app.route('/add')
def add_distraction():
    today = str(date.today())
    conn = sqlite3.connect("focus.db")
    cur = conn.cursor()

    cur.execute("SELECT distractions FROM focus WHERE date=?", (today,))
    row = cur.fetchone()

    if row:
        cur.execute(
            "UPDATE focus SET distractions = distractions + 1 WHERE date=?",
            (today,)
        )
    else:
        cur.execute(
            "INSERT INTO focus (date, distractions) VALUES (?, ?)",
            (today, 1)
        )

    conn.commit()
    conn.close()
    return redirect(url_for('home'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
