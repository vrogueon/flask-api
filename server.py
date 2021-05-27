from sqlite3 import Connection as SQLite3Connection
from datetime import datetime 
from sqlalchemy.engine import Engine
from flask import Flask, request, jsonify
from sqlalchemy import event
from flask_sqlalchemy import SQLAlchemy

# app
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://sqlitedb.file"
app.config["SQL_TRACK_MODIFICATIONS"] = 0

# config sqllite 3 to enforce foreing key constraints
@event.listens_for(Engine, "connect")
def _set_sqlite_pragma(dpai_connection, connection_record):
    if isinstance(dpai_connection, SQLite3Connection):
        cursor = dpai_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON;")
        cursor.close()

db = SQLAlchemy(app)
now = datetime.now

# models
class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50))
    address = db.Column(db.String(200))
    phone = db.Column(db.String(50))
    posts = db.relationship("BlogPost")

class BlogPost(db.Model):
    __tablename__ = "blog_post"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    body = db.Column(db.String(200))
    date = db.Column(db.Date)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
