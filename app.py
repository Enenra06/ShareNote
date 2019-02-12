from flask import Flask, render_template, request, redirect, url_for, session
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker
from users import User
from notes import Note
import sqlite3
import os

app = Flask(__name__, template_folder = '.')

@app.route('/')
def home():
    if session.get('logged'):
        return redirect(url_for('dashboard'))
    else:
        return render_template('index.html')

@app.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        form = request.form
        if form["password"] == form["retypepassword"]:
            engine = create_engine('sqlite:///users.db', echo = True)
            Session = sessionmaker(bind = engine)
            db_session = Session()
            owner = User(str(form["name"]), str(form["emailaddress"]), str(form["username"]), str(form["password"]))
            db_session.add(owner)
            db_session.commit()
            db_session.close()
            return redirect(url_for('login'))
        else:
            return render_template("register.html")
    else:
        return render_template("register.html")

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST' and session.get('logged') is None:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        query = 'SELECT password from users where username = \''+str(request.form["username"])+'\''
        result = cursor.execute(query).fetchall()
        cursor.close()
        if result[0][0] == request.form["password"]:
            session["logged"] = True
            session["username"] = request.form["username"]
            return redirect(url_for('dashboard'))
        else:
            return render_template("login.html")
    else:
        if session.get('logged'):
            return redirect(url_for('home'))
        else:
            return render_template('login.html')

@app.route('/dashboard', methods = ['GET', 'POST'])
def dashboard():
    if session.get('logged'):
        if request.method == 'POST':
            if isinstance(request.form.get('create_note'), unicode):
                engine = create_engine('sqlite:///notes.db', echo = True)
                Session = sessionmaker(bind = engine)
                db_session = Session()
                owner = Note(str(session.get("username")), str(request.form["name"]), str(request.form["body"]))
                db_session.add(owner)
                db_session.commit()
                db_session.close()
            elif isinstance(request.form.get('cancel_note'), unicode):
                conn = sqlite2.connect('notes.db')
                cursor = conn.cursor()
                query = 'DELETE from notes where id = \''+str(request.form["note_id"])+'\''
                cursor.execute(query).fetchall()
                conn.commit()
                cursor.close()         
            return redirect(url_for('home'))
        else:
            conn = sqlite3.connect('notes.db')
            cursor = conn.cursor()
            query = 'SELECT * from notes where owner = \''+str(session.get("username"))+'\''
            notes = cursor.execute(query).fetchall()
            conn.commit()
            cursor.close()
            return render_template('dashboard.html', notes = notes)  
    else:
        return redirect(url_for('home'))

@app.route('/notes/<number>', methods = ['GET', 'POST'])
def note(number):
    conn = sqlite3.connect('notes.db')
    cursor = conn.cursor()
    if request.method == 'POST':
        query = 'UPDATE notes SET name = \''+ request.form["name"]+'\', body = \''+ request.form["body"]+'\' WHERE id = \''+request.form["note_id"]+'\''
        cursor.execute(query)
        conn.commit()

    query = 'SELECT * from notes where id = \''+str(number)+'\''
    note = cursor.execute(query).fetchall()
    conn.commit()
    cursor.close()
    
    if note[0][1] == session.get("username"):
        print(note)
        return render_template('note.html', note = note)
    else:
        return redirect(url_for('home'))

@app.route('/logout')
def logout():
    if session.get('logged'):
        session.clear()
        return redirect(url_for('home'))

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True)
