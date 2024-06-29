def db_connection(app):
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = 'minionjc78#'
    app.config['MYSQL_DB'] = 'login_system'
    return app