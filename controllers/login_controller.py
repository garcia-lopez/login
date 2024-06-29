from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
#local imports
from models.users import *
from static.utils.utils import *

def login_function(mysql):
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username'].lower()
        password = request.form['password']

        account = verify_user(username, password, mysql)
        
        if account:
            # User is verified
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            return redirect(url_for('home'))
        else:
            # User not found, show error message
            flash('Usuario o contraseña incorrectos', 'error')
    
    return render_template('index.html')

def logout_function():
    if 'loggedin' in session:
        session.pop('loggedin')
        session.pop('id')
        session.pop('username')	
    return redirect(url_for('inicio'))