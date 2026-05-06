import sqlite3
import click
from flask import g, current_app


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE"],
            detect_types=sqlite3.PARSE_DECLTYPES,
        )
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db(app):
    app.teardown_appcontext(close_db)

    with app.app_context():
        db = get_db()
        db.executescript("""
            CREATE TABLE IF NOT EXISTS veiculos (
                id        INTEGER PRIMARY KEY AUTOINCREMENT,
                placa     TEXT    NOT NULL UNIQUE,
                marca     TEXT    NOT NULL,
                modelo    TEXT    NOT NULL,
                ano       INTEGER NOT NULL,
                cor       TEXT    NOT NULL,
                dono      TEXT    NOT NULL,
                criado_em TEXT    NOT NULL DEFAULT (datetime('now'))
            );
        """)
        db.commit()
