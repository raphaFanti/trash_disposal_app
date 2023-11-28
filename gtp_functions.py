import openai
import base64

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
