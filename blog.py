# blog.py - controller

# imports
from flask import Flask, render_template, request, session, flash, redirect, \
    url_for, g
from functools import wraps
import sqlite3

app = Flask(__name__)

# configuration (later found by Flask because written in UPPERCASE)
app.config.from_pyfile('settings.py')


def connect_db():
    """Connect to the database."""
    return sqlite3.connect(app.config['DATABASE'])


def login_required(test):
    """Return the method only if the user is logged in."""
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to log in first.')
            return redirect(url_for('login'))
    return wrap


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
    return render_template('login.html', error=error), status_code


@app.route('/logout')
def logout():
    """Return the logout page to the client."""
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('login'))


@app.route('/main')
@login_required
def main():
    """Return main page to the client."""
    g.db = connect_db()
    cur = g.db.execute('SELECT * FROM posts')
    posts = [dict(title=row[0], post=row[1]) for row in cur.fetchall()]
    print(posts)
    g.db.close()
    return render_template('main.html', posts=posts)


if __name__ == '__main__':
    app.run(debug=True)
