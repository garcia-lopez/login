# Description: This file is used to connect to the MySQL database.
# Please fill in the blanks with the correct credentials to connect to your database.
# Hardcoding credentials is not recommended, but for the sake of simplicity, I have done so.
def db_connection(app):
  app.config['MYSQL_HOST'] = 'localhost'
  app.config['MYSQL_USER'] = 'root'
  app.config['MYSQL_PASSWORD'] = 'minionjc78#'
  app.config['MYSQL_DB'] = 'login_system'
  return app
