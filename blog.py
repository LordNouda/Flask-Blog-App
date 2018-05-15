# blog.py - controller

# imports
from flask import Flask, render_template, request, session, flash, redirect, \
    url_for, g
import sqlite3

app = Flask(__name__)

# configuration (later found by Flask because written in UPPERCASE)
app.config.from_pyfile('settings.py')


# function used for connecting to the database
def connect_db():
    """Connect to the database."""
    return sqlite3.connect(app.config['DATABASE'])


@app.route('/', methods=['GET', 'POST'])
def login():
    """Return the login page to the client."""
    error = None
    status_code = 200
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username. Please try again.'
            status_code = 401
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password. Please try again.'
            status_code = 401
        else:
            session['logged_in'] = True
            return redirect(url_for('main'))
    print(error)
    return render_template('login.html', error=error)


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
