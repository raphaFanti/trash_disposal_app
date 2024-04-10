from flask import Flask
from flask_bootstrap import Bootstrap5
from flask_wtf import CSRFProtect
import secrets
import os
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .gcp_db_connector import connect_with_connector
from sqlalchemy.orm import Session

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
#gcp_connection = connect_with_connector(app.config["CLOUDSQL_INSTANCE_NAME"], app.config["CLOUDSQL_USER"], app.config["CLOUDSQL_PASSWORD"], app.config["CLOUDSQL_DATABASE"])

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql+pg8000://{db_user}:{db_password}@{host}/{db_name}".format(
    db_user=app.config["CLOUDSQL_USER"],
    db_password=app.config["CLOUDSQL_PASSWORD"],
    host=app.config["CLOUDSQL_INSTANCE_IP"],
    db_name="postgres"
)


db = SQLAlchemy(app)
#db.create_engine = gcp_connection.create_engine

#db = SQLAlchemy(app)
#db.create_engine = gcp_connection.create_engine


#db = SQLAlchemy(app)
#db.create_engine = engine

# Migrate setup
migrate = Migrate(app, db)

# Import routes
from app import routes, models