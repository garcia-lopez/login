import re
import bcrypt

def check_password(password):
    # General message for all requirements
    general_message = ("The password must be 8-72 characters long, include at least one lowercase letter, "
                       "one uppercase letter, one digit, and one special character.")
    # Check the password length and pattern requirements
    pattern = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*(),.?\":{}|<>]).{8,72}$")
    if not pattern.match(password):
        return False, general_message
    
    return True, "The password is secure."

def check_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None

def check_username(username):
    return re.match(r"^[a-zA-Z0-9_]+", username) is not None


def validate_user_input(email, username, password=None): 
    
    if password:
        valid, message = check_password(password)
        if not valid:
            return message
    if not check_email(email):
        return "The email is not valid."
    if not check_username(username):
        return "No special characters are allowed in the username."
    else: 
        return None

def val_password(plain_password, hashed_password):
    # Ensure both plain_password and hashed_password are in byte format
    byte_plain_password = plain_password.encode('utf-8')
    byte_hashed_password = hashed_password.encode('utf-8')  # Convert string to bytes

    # Use bcrypt.checkpw to compare the password with the hashed password
    return bcrypt.checkpw(byte_plain_password, byte_hashed_password)