from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
import os
import requests
from config.config_keys import APIkeys
import openai
import base64

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
Bootstrap(app)

# Add your OpenAI API key here
openai.api_key = APIkeys("openAI")


# Define routes and logic here
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Handle uploaded image here and use OpenAI API to get the trash disposal instructions
        image = request.files['image']
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
        image.save(image_path)
        
        image_validated, string = validate_image(image_path)
        
        if image_validated:
            return render_template("confirm_inputs.html", item_to_dispose = string, user_location = "Sunpaulo")
        else:
            return render_template("problem.html", error_message = string)

    return render_template('index.html')
    
def validate_image(image_path):
    '''
    Checks that the image uploaded has one main item
    '''
    try:
        # Read the image file as bytes
        with open(image_path, 'rb') as image_file:
            image_data = image_file.read()
            
        # Convert the image data to a base64-encoded string
        image_base64 = base64.b64encode(image_data).decode('utf-8')
        #image_base64 = image_data

        # Call the OpenAI API for image classification
        response = openai.Completion.create(
            engine="davinci",
            prompt=f"Identify the main object in this image: {image_base64}",
            max_tokens=10,  # You can adjust the maximum token count as needed
            n=1,  # Limit to 1 response
            stop=None,  # No stopping sequence
            temperature=0.7,  # You can adjust the temperature parameter
        )

        # Clean up uploaded image after processing
        os.remove(image_path)
        
        # Extract the label and confidence from the API response
        label = response.choices[0].text.strip()

        # Check if the response indicates one main item with high confidence
        if label:
            return True, label
        else:
            return False, "Unable to identify one main object with high confidence."

    except Exception as e:
        return False, str(e)
    

if __name__ == '__main__':
    app.run(debug = True)