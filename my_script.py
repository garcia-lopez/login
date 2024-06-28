import bcrypt

#I used this code to generate the hashed password for my test user in my database, 'cause yes, I'm lazy to do it manually

# The password to be hashed
password = "12345"

# Generate a salt and hash the password
salt = bcrypt.gensalt()
hashed_password = bcrypt.hashpw(password.encode(), salt)

# Print the hashed password
print(hashed_password.decode())