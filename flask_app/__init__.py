from flask import Flask
from flask_bcrypt import Bcrypt
import os
app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = os.environ.get('SESSION_SECRET_KEY')