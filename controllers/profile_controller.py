from flask import Flask, render_template, request, redirect, url_for, flash
#local imports
from models.users import *
from static.utils.utils import *

def profile_function(session, mysql):
    if 'loggedin' in session:
        accounts = user_info(session['id'],mysql) #obtener la información del usuario que ha iniciado sesión sesión para mostrarla
        session['user_info'] = accounts
        return render_template('profile.html', account=accounts)
    return redirect(url_for('login'))

def edit_profile_function(session, mysql):
    if 'loggedin' in session:
        if request.method == 'POST' and 'username' in request.form and 'email' in request.form:
            username = request.form['username']
            email = request.form['email']
            error = validate_user_input(email, username)
            
            if username == session['user_info']['username'] and email == session['user_info']['email']:
                flash('No se realizaron cambios', 'error')
            elif verify_user_already_exists(username, mysql) and username != session['user_info']['username']:
                flash('The username is already in use. Please choose another.', 'error')
            elif error:
                flash(error, 'error')
            else:
                update_user(session['id'], username, email, mysql)
                return redirect(url_for('profile'))
        return render_template('edit_profile.html', account=session['user_info'])
    return redirect(url_for('login'))

def change_password_function(session, mysql):
    if 'loggedin' in session:
        if request.method == 'POST' and 'old_password' in request.form and 'new_password' in request.form and 'confirm_password' in request.form:
            old_password = request.form['old_password']
            new_password = request.form['new_password']
            confirm_password = request.form['confirm_password']
            #Verifica si los campos están vacíos
            if old_password == '' or new_password == '' or confirm_password == '':
                flash('Please fill in all the fields', 'error')
                return render_template('change_password.html')
            
            #Verifica si la contraseña actual es correcta
            if not val_password(old_password, session['user_info']['password']):
                print("La contraseña actual es incorrecta")
                flash('The current password is incorrect.', 'error')
                return render_template('change_password.html')
            
            #Verifica si la nueva contraseña cumple con los requisitos
            valid, message = check_password(new_password)
            if not valid:
                print("La contraseña no cumple con los requisitos")
                flash(message, 'error')
            elif new_password != confirm_password:
                print("Las contraseñas no coinciden")
                flash('The passwords do not match.', 'error')
            #Si todo está bien, actualiza la contraseña
            else:
                update_password(session['id'], new_password, mysql)
                flash('Password successfully updated', 'success')

        return render_template('change_password.html')
    return redirect(url_for('login'))