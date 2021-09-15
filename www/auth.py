import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from . import dbconnect

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET','POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor, conn = dbconnect.connection()
        error = None

        if not username:
            error = "Username is required."
        elif not password:
            error = "Password is required."

        sql_query = """SELECT id FROM user WHERE username = %s"""
        cursor.execute(sql_query,(username,))
        record = cursor.fetchone()

        if record is not None:
            error = 'User {} is already registered.'.format(username)


        if error is None:
            sql_insert = """INSERT INTO user (username, password, key_pwd, salt) VALUES (%s, %s, %s, %s)"""
            #salt = os.urandom(32)
            #key_pwd = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
            key_pwd = 2131313
            salt = 12345
            password_hash = generate_password_hash(password)

            cursor.execute(sql_insert, (username, password_hash, key_pwd, salt))
            conn.commit()
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor, conn = dbconnect.connection()
        error = None
        try:
            sql_query = """SELECT * FROM user WHERE username = %s"""
            cursor.execute(sql_query, (username,))
            user = cursor.fetchone()

            if user is None:
                error = 'Incorrect username.'
            elif not check_password_hash(user[2], password):
                error = 'Incorrect password.'

            if error is None:
                session.clear()
                session['user_id'] = user[0]
                return redirect(url_for('index'))


        except Exception as e:
            print(str(e))

        flash(error)

    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        cursor, conn = dbconnect.connection()
        sql_query = """SELECT * FROM user WHERE id = %s"""
        cursor.execute(sql_query, (user_id,))
        g.user = cursor.fetchone()

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view