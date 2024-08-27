import os
from db import db
from flask import abort, request, session, flash
from sqlalchemy import text
from werkzeug.security import check_password_hash, generate_password_hash
from markupsafe import Markup
from datetime import datetime

def login(name, password):
    sql = text("SELECT password, id FROM users WHERE name=:name")
    result = db.session.execute(sql, {"name":name})
    user = result.fetchone()
    if not user:
        return False
    else:
        hash_value = user.password
        if check_password_hash(hash_value, password):
                session["user_id"] = user[1]
                session["user_name"] = name
                session["csrf_token"] = os.urandom(16).hex()
                session["logged_in"] = True
                if isAdmin(user.id):
                    session["is_admin"] = True
                    flash('Logged in as admin!', 'success')
                else:
                    session["is_admin"] = False
                    flash('Logged in!', 'success')
                return True
        else:
            return False

def comment(user_id, song_id, content):
    timestamp = datetime.now()
    sql = text("INSERT INTO comments (user_id, song_id, content, timestamp) VALUES (:user_id, :song_id, :content, :timestamp)")
    db.session.execute(sql, {"user_id":user_id, "song_id":song_id, "content":content, "timestamp":timestamp})
    db.session.commit()

def delete_comment(id):
    sql = text("DELETE FROM comments WHERE id=:id")
    db.session.execute(sql, {"id":id})
    db.session.commit()

def who_commented(id):
    sql = text("SELECT user_id FROM comments WHERE id=:id")
    result = db.session.execute(sql, {"id":id})
    user = result.fetchone()
    if not user:
        return None
    else:
        return user[0]

def register(name, artist_name, password):
    try:
        hash_value = generate_password_hash(password)
        sql = text("INSERT INTO users (name, artist_name, password) VALUES (:name, :artist_name, :password)")
        db.session.execute(sql, {"name":name, "artist_name":artist_name, "password":hash_value})
        db.session.commit()
    except:
        return False
    return True

def register_admin(name, artist_name, password):
    try:
        hash_value = generate_password_hash(password)
        sql = text("INSERT INTO users (name, artist_name, password, is_admin) VALUES (:name, :artist_name, :password, TRUE)")
        db.session.execute(sql, {"name":name, "artist_name":artist_name, "password":hash_value})
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
        description = desc[0].replace('\n', '<br>')
        description = Markup(description)
        return description

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
        hash_value = generate_password_hash(new_password)
        sql = text("UPDATE users SET password=:new_password WHERE id=:id")
        db.session.execute(sql, {"new_password":hash_value, "id":id})
        db.session.commit()
    except:
        return False
    return True    

def update_information(id, new_artistname, new_desc, old_password, new_password, new_password2):
    if new_artistname:
        if new_artistname != artist(id):
            if len(new_artistname) > 100:
                return False
            elif not change_artistname(id, new_artistname):
                return False
    if new_desc:
        if not change_desc(id, new_desc):
            return False
    if new_password:
        if old_password:
            if check_password_hash(password(id), old_password):
                if new_password == new_password2:
                    if not change_password(id, new_password):
                        return False
                else:
                    return False
            else:
                return False
    return True

def validate(id):
    sql = text("SELECT id FROM users WHERE id=:id")
    result = db.session.execute(sql, {"id":id})
    user = result.fetchone()
    if not user:
        return False
    else:
        return True

def user_exists(name):
    sql = text("SELECT name FROM users WHERE name=:name")
    result = db.session.execute(sql, {"name":name})
    user = result.fetchone()
    if not user:
        return False
    else:
        return True

def user_id_exists(id):
    sql = text("SELECT id FROM users WHERE id=:id")
    result = db.session.execute(sql, {"id":id})
    user = result.fetchone()
    if not user:
        return False
    else:
        return True

def isAdmin(id):
    sql = text("SELECT is_admin FROM users WHERE id=:id")
    result = db.session.execute(sql, {"id":id})
    user = result.fetchone()
    if user.is_admin:
        return True
    else:
        return False