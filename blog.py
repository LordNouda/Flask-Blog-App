# blog.py - controller

# imports
from flask import Flask, render_template, request, session, flash, redirect, \
    url_for, g
import sqlite3

# configuration (later found by Flask because written in UPPERCASE)
DATABASE = 'blog.db'
USERNAME = 'admin'
PASSWORD = 'admin'
SECRET_KEY = "4tS%qLWn"


app = Flask(__name__)

# pulls in app configuration by looking for UPPERCASE variables
app.config.from_object(__name__)


# function used for connecting to the database
def connect_db():
    """Connect to the database."""
    return sqlite3.connect(app.config['DATABASE'])


@app.route('/', methods=['GET', 'POST'])
def login():
    """Return the loginpage to the client."""
    error = None
    status_code = 200
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME'] or \
                request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid Credentials. Please try again.'
            status_code = 401
        else:
            session['logged_in'] = True
            return redirect(url_for('main'))
    return render_template('login.html')


@app.route('/logout')
def logout():
    """Return the logout page to the client."""
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('login'))


@app.route('/main')
def main():
    """Return main page to the client."""
    return render_template('main.html')


if __name__ == '__main__':
    app.run(debug=True)
