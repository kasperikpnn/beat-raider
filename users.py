import os
from flask import abort, request, session
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import text

def login(name, password):
    from db import db
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
    from db import db
    try:
        sql = text("INSERT INTO users (name, artist_name, password) VALUES (:name, :artist_name, :password)")
        db.session.execute(sql, {"name":name, "artist_name":artist_name, "password":password})
        db.session.commit()
    except:
        return False
    return True

def whois(id):
    from db import db
    sql = text("SELECT name FROM users WHERE id=:id")
    result = db.session.execute(sql, {"id":id})
    user = result.fetchone()
    if not user:
        return "Error"
    else:
        return user[0]

def artist(id):
    from db import db
    sql = text("SELECT artist_name FROM users WHERE id=:id")
    result = db.session.execute(sql, {"id":id})
    user = result.fetchone()
    if not user:
        return "Error"
    else:
        return user[0]