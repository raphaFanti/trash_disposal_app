from google.cloud import vision
from google.cloud import storage
from PIL import Image
import io
from datetime import datetime, timedelta


class ImageHandler():
    '''
    Class to handle image uploads and object identification
    '''

    def __init__(self, image_file):
        self.image_file = Image.open(io.BytesIO(image_file.read()))
        self.upload_client = storage.Client()
        self.annotation_client = vision.ImageAnnotatorClient()

    def pretreat_image(self, max_width = 800, max_height = 600, quality = 70):
        '''
        Pre-treats the image by resizing and compressing it
        '''

         # Get the current size of the image
        width, height = self.image_file.size

        # Calculate the aspect ratio
        aspect_ratio = width / height

        # Resize the image while preserving aspect ratio
        if width > max_width or height > max_height:
            if width / max_width > height / max_height:
                new_width = max_width
                new_height = int(max_width / aspect_ratio)
            else:
                new_height = max_height
                new_width = int(max_height * aspect_ratio)
            img = self.image_file.resize((new_width, new_height))

        # Compress image
        img_io = io.BytesIO()
        img.save(img_io, format='JPEG', quality = quality)
        img_io.seek(0) # Reset file pointer to the beginning

        # Point object attribute to compressed image
        self.image_file = img_io

    def upload_image(self, bucket_name):
        '''
        Uploads the image to the upload bucket and makes a signed url to the image
        '''

        # Create a blob
        bucket = self.upload_client.get_bucket(bucket_name)
        now = datetime.utcnow()
        timestamp = now.strftime("%Y%m%d_%H%M%S_%f")
        blob_name = f"image_{timestamp}.jpg"
        blob = bucket.blob(blob_name)
        
        # Upload file to blob
        blob.upload_from_file(self.image_file, content_type='image/jpeg')
        self.blob_name = blob_name
        self.image_file = None # removes file from object

        # Gets uri to uploaded image
        expiration = datetime.utcnow() + timedelta(seconds = 60 * 5)
        signed_url = blob.generate_signed_url(expiration = expiration)
        self.image_uri = signed_url

        return signed_url

    def get_main_objects(self, max_objects = 5, verbose = False):
        '''
        Gets the main objects in a picture using Google Cloud Vision API
        '''
        # Prepare image source
        image = vision.Image()
        image.source.image_uri = self.image_uri

        # Perform label detection on the image file
        response = self.annotation_client.label_detection(image = image)
        labels = response.label_annotations
        
        if verbose:
            print("Labels found:")
            for label in labels:
                print("{} : {}".format(label.description, label.score))

            if response.error.message:
                raise Exception(
                    "{}\nFor more info on error messages, check: "
                    "https://cloud.google.com/apis/design/errors".format(response.error.message)
            )
        
        return labels