import json
import os
from flask import Flask, render_template, request, redirect, flash, session, url_for, Response
from forms import UploadForm, ConfirmInputForm
from werkzeug.utils import secure_filename
from gVision_functions import get_main_objects
from gtp_functions import get_disposable_item
from flask_bootstrap import Bootstrap

app = Flask(__name__)

allowed_image_extensions = {'png', 'jpg', 'jpeg', 'gif', 'heic'}

# Load comuni
with open("comuni.json", "r") as f:
    comuni_full = json.load(f)
comuni = [c["nome"] for c in comuni_full]

@app.route('/_autocomplete', methods=['GET'])
def autocomplete():
    return Response(json.dumps(comuni), mimetype='application/json')

# Views
@app.route('/', methods=['GET', 'POST'])
def index():
    form = UploadForm() #try request.form

    if form.validate_on_submit():
        image = request.files['image']
        
        # Checks whether extension is allowed
        extension_allowed = image.filename.rsplit('.', 1)[1].lower() in allowed_image_extensions

        if not extension_allowed:
            flash("File type not supported") #ToDo: implement flash messages printing
            return redirect(url_for('index'))

        # Saves image
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
        image.save(image_path)
        
        # Understands objects in image
        image_objects = get_main_objects(image_path, max_objects = 5)

        # Figues out if there is a disposable object in the image
        disposable_object = get_disposable_item(image_objects, key=app.config['OPENAI_KEY'])
        
        # ToDo: Manage file deletion / persistence
        #os.remove(image_path)

        if disposable_object != "I don't know":
            session['image_url'] = image_path
            session['item_to_dispose'] = disposable_object
            return redirect(url_for('confirm_inputs'))
        else:
            # ToDo: To be implemented
            return render_template("problem.html", error_message=disposable_object)
        
    return render_template('index.html',  form=form)

@app.route('/confirm_inputs', methods=['GET', 'POST'])
def confirm_inputs():
    form = ConfirmInputForm()

    if form.validate_on_submit():
        if form.input_field != "":
            return redirect(url_for('index'))
        else:
            return render_template("problem.html", error_message="test no change in text")
        
    return render_template("confirm_inputs.html", image_url=session["image_url"], item_to_dispose=session["item_to_dispose"], form=form)

#@app.route('/problem', methods=['POST'])