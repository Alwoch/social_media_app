from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_tables(app):
    """initialise the app with the sqlalchemy extension and create tables"""
    db.init_app(app)
    with app.app_context():
        db.create_all()