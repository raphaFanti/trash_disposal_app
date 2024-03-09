from flask_bootstrap import Bootstrap5
from flask_wtf import CSRFProtect
import secrets
from config import Config

from app import app

app.config.from_object(Config)
# app.config.from_object('config.LocalConfig')
app.config['SECRET_KEY'] = secrets.token_urlsafe(16)
# Bootstrap-Flask requires this line
bootstrap = Bootstrap5(app)
# Flask-WTF requires this line
csrf = CSRFProtect(app)

app.run(host='0.0.0.0', debug=True)