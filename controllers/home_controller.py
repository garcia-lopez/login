from flask import render_template, redirect, url_for

def home_function(session):
    if 'loggedin' in session:
        print(session['username']	)
        return render_template('home.html', username=session['username'].capitalize())
    return redirect(url_for('login'))