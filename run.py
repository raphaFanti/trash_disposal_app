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

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)