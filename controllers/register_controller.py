from flask import Flask, render_template, request, redirect, url_for, flash
#local imports
from models.users import *
from static.utils.utils import *

def register_function(mysql):
     #Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # crear variables para una fácil escritura
        username = request.form['username'].lower()
        password = request.form['password']
        email = request.form['email']
        # Validate the input
        error = validate_user_input(email,username,password)
        print(error)
        if error:
            flash(error, 'error')
            return render_template('register.html')

        if not verify_user_already_exists(username, mysql):
        # If account does not exist, create a new account
         create_user(username, password, email,mysql)
         return redirect(url_for('login'))
        else:
            # Si el usuario ya existe, envía un mensaje flash
          flash('The username is already in use. Please choose another.', 'error')

    elif request.method == 'POST':
        # Form is empty... (no POST data)
        flash('Please fill out the form!')
    
    return render_template('register.html')
