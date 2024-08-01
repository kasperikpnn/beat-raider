import os
from db import db
from flask import abort, request, session
from sqlalchemy import text
from werkzeug.security import check_password_hash, generate_password_hash


def login(name, password):
    sql = text("SELECT password, id FROM users WHERE name=:name AND password=:password")
    result = db.session.execute(sql, {"name":name, "password":password})
    user = result.fetchone()
    if not user:
        return False
    session["user_id"] = user[1]
    session["user_name"] = name
    session["csrf_token"] = os.urandom(16).hex()
    return True

def register(name, artist_name, password):
    try:
        sql = text("INSERT INTO users (name, artist_name, password) VALUES (:name, :artist_name, :password)")
        db.session.execute(sql, {"name":name, "artist_name":artist_name, "password":password})
        db.session.commit()
    except:
        return False
    return True

def register_admin(name, artist_name, password):
    try:
        sql = text("INSERT INTO users (name, artist_name, password, is_admin) VALUES (:name, :artist_name, :password, TRUE)")
        db.session.execute(sql, {"name":name, "artist_name":artist_name, "password":password})
        db.session.commit()
    except:
        return False
    return True

def whois(id):
    sql = text("SELECT name FROM users WHERE id=:id")
    result = db.session.execute(sql, {"id":id})
    user = result.fetchone()
    if not user:
        return "Error"
    else:
        return user[0]

def artist(id):
    sql = text("SELECT artist_name FROM users WHERE id=:id")
    result = db.session.execute(sql, {"id":id})
    user = result.fetchone()
    if not user:
        return "Error"
    else:
        return user[0]