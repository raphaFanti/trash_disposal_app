import json
from app import app

app.config.from_file('config.json', load = json.load)

app.run(host='0.0.0.0', debug=True)