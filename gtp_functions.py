import openai

def set_key_chatGtp(api_key):
    openai.api_key = api_key
    return

def get_disposable_item(labels):
    '''
    Asks Chat GTP to return which item from a list is the item the user is trying to dispose of.
    '''

    question = '''
    The following labels have been identified via Google Vision API' Label Detection on an image
    uploaded by a user trying to dispose of an item in the trash. From the list which could be the item?
    Each row correspond to a label, its score (confidence in the label - 0 for low, 1 for high) and its topicality (importance in the image)
    In looking for the item, give high importance to labels that contain a material. For example "glass bottle" is more insightful than just "bottle".
    In case you identify the object respond simply its label without any additional text. In case you cannot identify a trashable object respond "I don't know".
    '''
    for label in labels:
        entry = (". Label: {}, Score: {}, Topicality: {}").format(label.description, label.score, label.topicality)
        question +=  entry + "\n"
    
    response = openai.chat.completions.create(
    model="gpt-3.5-turbo-1106",
    messages=[
        {"role": "system", "content": "You are a helpful assistant designed to help users dispose of items in the trash."},
        {"role": "user", "content": question}
    ]
    )
    return response.choices[0].message.content

def get_disposal_guidance(object_to_dispose, location):
    '''
    Asks ChatGTP how to dispose of an item in certain location
    '''

    question = '''
    The user is trying to dispose of an item in the trash in the below location, which should be a 'comune' (municipality) in Italy.
    In a typical municipality in Italy the bins are: umido (organic matter), carta (paper), plastica (plastic), metalli (metal), vetro (glass), secco (non-recyclable); but this changes depending on the municipality.
    Based on what you know, which of the above bins should the user throw it in?
    It may be that it is not possible to dispose of the item at home. For example used car oil is not disposable in any of the above bins. In that case respond 'Not possible to dispose at home"
    As much as possible try to give information relative to the user's location.
    '''
    question += "Location: " + location + "\n"
    question += "Object to dispose: " + object_to_dispose + "\n"

    response = openai.chat.completions.create(
    model="gpt-3.5-turbo-1106",
    messages=[
        {"role": "system", "content": "You are a helpful assistant designed to help users dispose of items in the trash."},
        {"role": "user", "content": question}
    ]
    )
    return response.choices[0].message.content