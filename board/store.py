import sqlite3

import click
from flask import g, current_app


def init_app(app):
    app.cli.add_command(init_db_command)


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db


@click.command('init-db')
def init_db_command():
    db = get_db()
    with current_app.open_resource('schema.sql') as f:
        db.cursor().executescript(f.read().decode("utf-8"))
    click.echo("Database successfully initialized.")
