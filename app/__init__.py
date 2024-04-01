from flask import Flask
from flask_bootstrap import Bootstrap5
from flask_wtf import CSRFProtect
import secrets
import os
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

# Configuration
app.config.from_object(Config)
app.config['SECRET_KEY'] = secrets.token_urlsafe(16)

# Bootstrap setup
bootstrap = Bootstrap5(app)

# Flask-WTF protection
csrf = CSRFProtect(app)

# Authentication to GCP
#gcp_credentials_path = os.path.join(app.root_path, app.config['GOOGLE_API_CREDENTIALS_FILENAME'])
gcp_credentials_path = app.config['GOOGLE_API_CREDENTIALS_FILENAME']
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = gcp_credentials_path

# DB connection
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Import routes
from app import routes, models