from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
#local imports
from models.users import *
from utils import *
app = Flask(__name__)

app.secret_key = 'shape_of_water'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'minionjc78#'
app.config['MYSQL_DB'] = 'login_system'

#print("MYSQL_HOST:", app.config['MYSQL_HOST'])
#print("MYSQL_USER:", app.config['MYSQL_USER'])
#print("MYSQL_PASSWORD:", app.config['MYSQL_PASSWORD'])
#print("MYSQL_DB:", app.config['MYSQL_DB'])

# Initialize Limiter
limiter = Limiter(
        get_remote_address,
        app=app,
        default_limits=["200 per day", "50 per hour"],
        storage_uri="memory://",
)

#Inicializar la conexión a la base de datos
mysql = MySQL(app)

@app.route('/login/', methods=['GET', 'POST'])
@limiter.limit("5 per minute")  # Limit request to 5 per minute
def login():
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

@app.route('/')
def inicio():
    return render_template('landing.html')

@app.route('/logout/')
def logout():
    if 'loggedin' in session:
        session.pop('loggedin')
        session.pop('id')
        session.pop('username')	
    return redirect(url_for('inicio'))

@app.route('/home/')
def home():
    if 'loggedin' in session:
        print(session['username']	)
        return render_template('home.html', username=session['username'].capitalize())
    return redirect(url_for('login'))

# Manejar errores de forma personalizada, para que muestra una página personalizada en lugar de la página de error predeterminada
@app.errorhandler(429)
def ratelimit_handler(e):
    return render_template('429.html'), 429

@app.route('/register/', methods=['GET', 'POST'])
def register():
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
          flash('El nombre de usuario ya está en uso. Por favor, elige otro.', 'error')

    elif request.method == 'POST':
        # Form is empty... (no POST data)
        flash('Please fill out the form!')
    
    return render_template('register.html')
    
@app.route('/profile/')
def profile():
    if 'loggedin' in session:
        accounts = user_info(session['id'],mysql) #obtener la información del usuario que ha iniciado sesión sesión para mostrarla
        session['user_info'] = accounts
        return render_template('profile.html', account=accounts)
    return redirect(url_for('login'))

@app.route('/edit_profile/', methods=['GET', 'POST'])
def edit_profile():
    if 'loggedin' in session:
        if request.method == 'POST' and 'username' in request.form and 'email' in request.form:
            username = request.form['username']
            email = request.form['email']
            error = validate_user_input(email, username)
            print(username)
            lol = verify_user_already_exists(username, mysql)
            print(lol)

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

@app.route('/change_password/', methods=['GET', 'POST'])
def change_password():
    print("hola")
    if 'loggedin' in session:
        if request.method == 'POST' and 'old_password' in request.form and 'new_password' in request.form and 'confirm_password' in request.form:
            old_password = request.form['old_password']
            new_password = request.form['new_password']
            confirm_password = request.form['confirm_password']
            if old_password == '' or new_password == '' or confirm_password == '':
                flash('Por favor, rellena todos los campos', 'error')
                return render_template('change_password.html')
            #Asegúrate de que la contraseña actual sea correcta y que las nuevas contraseñas coincidan
            if not val_password(old_password, session['user_info']['password']):
                print("La contraseña actual es incorrecta")
                flash('The current password is incorrect.', 'error')
            elif new_password != confirm_password:
                print("Las contraseñas no coinciden")
                flash('The passwords do not match.', 'error')
            #Si todo está bien, actualiza la contraseña
            else:
                update_password(session['id'], new_password, mysql)
                flash('Password successfully updated', 'success')

        return render_template('change_password.html')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)