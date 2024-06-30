from flask import Flask, render_template, session
from flask_mysqldb import MySQL

#local imports
from models.users import *
from static.utils.utils import *
from connection.mysql_connection import  db_connection
from connection.limiter import limit_time
from controllers.login_controller import login_function, logout_function
from controllers.home_controller import home_function
from controllers.register_controller import register_function
from controllers.profile_controller import edit_profile_function, profile_function, change_password_function
app = Flask(__name__)

app.secret_key = 'shape_of_water'

app = db_connection(app)

#Inicializar la conexión a la base de datos
mysql = MySQL(app)

#Inicializar el límite de solicitudes
limiter = limit_time(app)

@app.route('/')
def inicio():
    return render_template('landing.html')

@app.route('/login/', methods=['GET', 'POST'])
@limiter.limit("5 per minute")  # Limit request to 5 per minute
def login():
    return login_function(mysql)


@app.route('/logout/')
def logout():
    return logout_function()


@app.route('/home/')
def home():
    return home_function(session)


# Manejar errores de forma personalizada, para que muestre una página personalizada en lugar de la página de error predeterminada
@app.errorhandler(429)
def ratelimit_handler(e):
    return render_template('429.html'), 429

@app.route('/register/', methods=['GET', 'POST'])
def register():
    return register_function(mysql)
   
    
@app.route('/profile/')
def profile():
    return profile_function(session, mysql)


@app.route('/edit_profile/', methods=['GET', 'POST'])
def edit_profile():
    return edit_profile_function(session, mysql)

@app.route('/change_password/', methods=['GET', 'POST'])
def change_password():
    return change_password_function(session, mysql)


if __name__ == '__main__':
    app.run(debug=True)