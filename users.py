import os
from db import db
from flask import abort, request, session
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import text

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