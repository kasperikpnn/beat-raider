import random
import string
BASE64_CHARS = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_'
BASE64_LENGTH = len(BASE64_CHARS)
ID_LENGTH = 10
from sqlalchemy import text
from flask import abort, request, session
import os

def generate_id():
    id = ''.join(random.choice(BASE64_CHARS) for _ in range(ID_LENGTH))
    if id_exists(id):
        generate_id()
    return id

def id_exists(id):
    from db import db
    sql = text("SELECT id FROM songs")
    result = db.session.execute(sql)
    if id in result:
        return True
    return False