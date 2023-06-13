import psycopg2

import click
from flask import current_app, g

#TODO refactor this function
def get_db():
    if 'db' not in g:
        url=current_app.config['DATABASE']
        connection=psycopg2.connect(url)
        cursor=connection.cursor()

        return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()

    with current_app.open_resource('models.sql') as m:
        db.executescript(m.read().decode('utf8'))


@click.command('init-db')
def init_db_command():
    """clear the existing data and create new tables"""
    init_db()
    click.echo('initialised the database')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
