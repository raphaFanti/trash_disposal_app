from openai import OpenAI


def get_disposable_item(labels, key, verbose = True):
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
    
    client = OpenAI(api_key = key)
    response = client.chat.completions.create(
    model="gpt-3.5-turbo-1106",
    messages=[
        {"role": "system", "content": "You are a helpful assistant designed to help users dispose of items in the trash."},
        {"role": "user", "content": question}
    ]
    )
    return response.choices[0].message.content