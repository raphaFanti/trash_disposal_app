from openai import OpenAI


def get_disposable_item(labels, key, verbose = True):
    '''
    Asks Chat GTP to return which item from a list is the item the user is trying to dispose of.
    '''

    question = '''
    The following labels have been identified via a naural network in a picture
    uploaded by a user trying to dispose of an item in the trash. From the list which could be the item?
    Respond with the entire original label in case you identiy the disposable item, otherwise respond none.\n
    '''
    for label in labels:
        question += ". " + label.description + "\n"

    print(question)

    client = OpenAI(api_key=key)
    response = client.chat.completions.create(
    model="gpt-3.5-turbo-1106",
    response_format={ "type": "json_object" },
    messages=[
        {"role": "system", "content": "You are a helpful assistant designed to output JSON."},
        {"role": "user", "content": question}
    ]
    )
    print(response.choices[0].message.content)