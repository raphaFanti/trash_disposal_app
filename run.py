import json
from flask_bootstrap import Bootstrap5
from flask_wtf import CSRFProtect
import random
import string

from app import app

import secrets
foo = secrets.token_urlsafe(16)
app.secret_key = foo

# Bootstrap-Flask requires this line
bootstrap = Bootstrap5(app)
# Flask-WTF requires this line
csrf = CSRFProtect(app)


app.config.from_file('config.json', load = json.load)

app.run(host='0.0.0.0', debug=True)