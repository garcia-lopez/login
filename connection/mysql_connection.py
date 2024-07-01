# Description: This file is used to connect to the MySQL database.
# Please fill in the blanks with the correct credentials to connect to your database.
def db_connection(app):
    app.config['MYSQL_HOST'] = ''
    app.config['MYSQL_USER'] = ''
    app.config['MYSQL_PASSWORD'] = ''
    app.config['MYSQL_DB'] = ''
    return app