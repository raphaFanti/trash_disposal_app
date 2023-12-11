import json
from gVision_functions import get_main_objects
from gtp_functions import get_disposable_item

class testPicture(picture_path):
  # Sends image to Google Vision API to gets its labels
  test_img_path = "C:/Users/rapha/trash_disposal_app/trash_disposal_app/upload_folder/test-image.jpg"
  labels = get_main_objects(test_img_path, 10, verbose = True)

  # Asks Chat GTP to get which item is the one user is trying to dispose of
  with open('config.json') as config_file:
    file_contents = config_file.read()
  key = json.loads(file_contents)["openAI_key"]

  disposable_obj = get_disposable_item(labels = labels, verbose = True, key = key)