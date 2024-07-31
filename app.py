from flask import Flask
from flask import redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import os
from song_manager import SongManager

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
SM = SongManager(upload_folder=os.path.join(app.root_path, 'uploads'))

import routes