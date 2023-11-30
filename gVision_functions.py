from google.cloud import vision

def get_main_objects(image_path, max_objects = 5, verbose = False):
    '''
    Gets the main objects in a picture using Google Cloud Vision API
    '''

    client = vision.ImageAnnotatorClient()

    with open(image_path, "rb") as image_file:
        content = image_file.read()
    image = vision.Image(content=content)

    response = client.label_detection(image=image)
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