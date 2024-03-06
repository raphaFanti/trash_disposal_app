import json
import os
from flask import Flask, render_template, request, redirect, flash, session, url_for, Response
from forms import UploadForm, ConfirmInputForm, UserFeedbackForm
from werkzeug.utils import secure_filename
from gVision_functions import get_main_objects
from gtp_functions import set_key_chatGtp, get_disposable_item, get_disposal_guidance

app = Flask(__name__)

allowed_image_extensions = {'png', 'jpg', 'jpeg', 'gif', 'heic'}

# Comuni autocomplete
with open("comuni.json", "r") as f:
    comuni_full = json.load(f)
comuni = [c["nome"] for c in comuni_full]

@app.route('/_autocomplete', methods=['GET'])
def autocomplete():
    return Response(json.dumps(comuni), mimetype='application/json')

# App routes
@app.route('/', methods=['GET', 'POST'])
def index():
    form = UploadForm()

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
        set_key_chatGtp(app.config['OPENAI_KEY'])
        disposable_object = get_disposable_item(image_objects)
        
        # ToDo: Manage file deletion / persistence
        #os.remove(image_path)

        if disposable_object != "I don't know":
            session['image_url'] = image_path
            session['item_to_dispose'] = disposable_object
            session['dispose_location'] = request.form["dispose_location"]
            return redirect(url_for('confirm_inputs'))
        else:
            # ToDo: To be improved
            return render_template("problem.html", error_message="No item to dispose found in image")
        
    return render_template('index.html',  form=form)

@app.route('/confirm_inputs', methods=['GET', 'POST'])
def confirm_inputs():
    form = ConfirmInputForm()

    if form.validate_on_submit():
        
        # User accepted proposed object
        if "confirm_input" in request.form:
            return redirect(url_for("disposal_guidance", 
                                    object_to_dispose = session["item_to_dispose"],
                                    place = session['dispose_location'])
                                    )
        
        # User refused proposed object
        else:
            proposed_object = request.form["input_field"]
            
            # User has provided a proposed object
            if proposed_object != "":
                session["user_proposed_object"] = proposed_object
                return redirect(url_for("disposal_guidance", 
                                    object_to_dispose = proposed_object,
                                    place = session['dispose_location'])
                                    )

            # User has not provided an alternative object
            else:
                flash("Prego esplicitare un oggetto da buttare se quello proposto da ChatGPT non è giusto")
                return redirect(url_for('confirm_inputs'))
        
    return render_template("confirm_inputs.html", image_url=session["image_url"], item_to_dispose=session["item_to_dispose"], form=form)

@app.route('/disposal_guidance/<object_to_dispose>/<place>', methods=['GET', 'POST'])
def disposal_guidance(object_to_dispose = None, place = "Italy"):
    
    # Sends to index in case no object is supplied
    if object_to_dispose == None:
        flash("Prego fornire una foto del oggetto da butare")
        return redirect(url_for("index"))

    # Gets disposal guidance
    else:
        guidance = get_disposal_guidance(object_to_dispose, place)

    form = UserFeedbackForm()

    if form.validate_on_submit():
        # User accepted proposed object
        if "confirm_input" in request.form:
            flash("Grazie del vostro feedback!")
            return redirect(url_for("index"))
        
        # User refused proposed object
        else:
            proposed_bin = request.form["input_field"]
            
            # User has provided a proposed object
            if proposed_bin != "":
                session["user_proposed_bin"] = proposed_bin # need to put this in app log
                flash("Grazie del vostro feedback! Investigueremo la vostra proposta.")
                return redirect(url_for("index"))

            # User has not provided an alternative object
            else:
                flash("Prego esplicitare dove buttare se la proposta da ChatGPT non è giusta")
                return redirect(url_for('guidance'))


    return render_template("guidance.html", disposal_guidance=guidance, form=form)