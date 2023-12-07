import os
from flask import Flask, render_template, request
from forms import UploadForm
from gVision_functions import get_main_objects
from gtp_functions import get_disposable_item

app = Flask(__name__)

# Define routes and logic here
@app.route('/', methods=['GET', 'POST'])
def index():
    form = UploadForm()
    if request.method == 'POST':

        image = request.files['image']
        image_path = os.path.join(app.config['upload_folder'], image.filename)
        image.save(image_path)
        
        image_objects = get_main_objects(image_path, max_objects = 5)
        disposable_objects = get_disposable_item(image_objects)
        
        if len(disposable_objects) > 0:
            return render_template("confirm_inputs.html", item_to_dispose = string, user_location = "Sunpaulo")
        else:
            return render_template("problem.html", error_message = string)
        
    return render_template('index.html',  form = form)