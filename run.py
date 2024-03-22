from flask_bootstrap import Bootstrap5
from flask_wtf import CSRFProtect
import secrets
import os

from config import Config

from app import app

app.config.from_object(Config)
app.config['SECRET_KEY'] = secrets.token_urlsafe(16)
# Bootstrap-Flask requires this line
bootstrap = Bootstrap5(app)
# Flask-WTF requires this line
csrf = CSRFProtect(app)
# Authentication to GCP
gcp_credentials_path = os.path.join(app.root_path, app.config['GOOGLE_API_CREDENTIALS_FILENAME'])
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = gcp_credentials_path

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)