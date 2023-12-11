import json
import os
from flask import Flask, render_template, request, redirect, flash, url_for, Response
from forms import UploadForm
from werkzeug.utils import secure_filename
from gVision_functions import get_main_objects
from gtp_functions import get_disposable_item

app = Flask(__name__)

allowed_image_extensions = {'png', 'jpg', 'jpeg', 'gif', 'heic'}

cities = ["Bratislava",
          "Banská Bystrica",
          "Prešov",
          "Považská Bystrica",
          "Žilina",
          "Košice",
          "Ružomberok",
          "Zvolen",
          "Poprad"]

@app.route('/_autocomplete', methods=['GET'])
def autocomplete():
    return Response(json.dumps(cities), mimetype='application/json')

# Define routes and logic here
@app.route('/', methods=['GET', 'POST'])
def index():
    form = UploadForm() #try request.form

    if form.validate_on_submit():
        image = request.files['image']
        
        # Checks whether extension is allowed
        extension_allowed = image.filename.rsplit('.', 1)[1].lower() in allowed_image_extensions

        if not extension_allowed:
            flash("File type not supported")
            return redirect(url_for('index'))

        # Saves image
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
        image.save(image_path)
        
        # Understands objects in image
        image_objects = get_main_objects(image_path, max_objects = 5)

        # Figues out if there is a disposable object in the image
        disposable_objects = get_disposable_item(image_objects, key=app.config['OPENAI_KEY'])
        
        # Deletes image
        #os.remove(image_path)

        if len(disposable_objects) > 0:
            return render_template("confirm_inputs.html", item_to_dispose=disposable_objects[0])
        else:
            return render_template("problem.html", error_message=disposable_objects[0])
        
    return render_template('index.html',  form=form)