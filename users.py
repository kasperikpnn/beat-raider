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
        sql = text("INSERT INTO users (name, artist_name, password, description) VALUES (:name, :artist_name, :password, 'No description set')")
        db.session.execute(sql, {"name":name, "artist_name":artist_name, "password":password})
        db.session.commit()
    except:
        return False
    return True

def register_admin(name, artist_name, password):
    try:
        sql = text("INSERT INTO users (name, artist_name, password, description, is_admin) VALUES (:name, :artist_name, :password, 'No description set', TRUE)")
        db.session.execute(sql, {"name":name, "artist_name":artist_name, "password":password})
        db.session.commit()
    except:
        return False
    return True

def whois(id):
    sql = text("SELECT artist_name FROM users WHERE id=:id")
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
    
def desc(id):
    sql = text("SELECT description FROM users WHERE id=:id")
    result = db.session.execute(sql, {"id":id})
    desc = result.fetchone()
    if not desc:
        return "Error"
    else:
        return desc[0]

def change_artistname(id, new_artistname):
    try:
        sql = text ("UPDATE users SET artist_name=:new_artistname WHERE id=:id")
        db.session.execute(sql, {"new_artistname":new_artistname, "id":id})
        db.session.commit()
    except:
        return False
    return True

def change_desc(id, new_desc):
    try:
        sql = text ("UPDATE users SET description=:new_desc WHERE id=:id")
        db.session.execute(sql, {"new_desc":new_desc, "id":id})
        db.session.commit()
    except:
        return False
    return True    

def password(id):
    sql = text("SELECT password FROM users WHERE id=:id")
    result = db.session.execute(sql, {"id":id})
    pw = result.fetchone()
    if not pw:
        return None
    else:
        return pw[0]
    
def change_password(id, new_password):
    try:
        sql = text ("UPDATE users SET password=:new_password WHERE id=:id")
        db.session.execute(sql, {"new_password":new_password, "id":id})
        db.session.commit()
    except:
        return False
    return True    

def update_information(id, new_artistname, new_desc, old_password, new_password, new_password2):
    if new_artistname:
        if new_artistname != artist(id):
            if len(new_artistname) > 100:
                return "Artist name is too long!"
            elif not change_artistname(id, new_artistname):
                return "Error with changing the artist name"
    if new_desc:
        if new_desc != desc(id):
            if not change_desc(id, new_desc):
                return "Error with changing the description"
    if new_password:
        if old_password:
            if old_password == password(id):
                if new_password == new_password2:
                    if not change_password(id, new_password):
                        return "Error with changing the password"
    return ""

def validate(id):
    sql = text("SELECT id FROM users WHERE id=:id")
    result = db.session.execute(sql, {"id":id})
    user = result.fetchone()
    if not user:
        return False
    else:
        return True

    