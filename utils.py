import re
import bcrypt

def check_password(password):
    return len(password) <= 72 # To use the hash library the password must be less 72 characters long 

def check_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None

def check_username(username):
    return re.match(r"^[a-zA-Z0-9_]+", username) is not None


def validate_user_input(email, username, password=None): 
    if password is not None and not check_password(password):
        return "La contraseña no puede ser mayor a 72 caracteres."
    if not check_email(email):
        return "El correo no es válido."
    if not check_username(username):
        return "El nombre de usuario no es válido."
    else: 
        return None

def val_password(plain_password, hashed_password):
    # Ensure both plain_password and hashed_password are in byte format
    byte_plain_password = plain_password.encode('utf-8')
    byte_hashed_password = hashed_password.encode('utf-8')  # Convert string to bytes

    # Use bcrypt.checkpw to compare the password with the hashed password
    return bcrypt.checkpw(byte_plain_password, byte_hashed_password)