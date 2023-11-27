import os
from dotenv import load_dotenv, find_dotenv
from dataclasses import dataclass

load_dotenv(find_dotenv())
@dataclass(frozen=True)
class APIkeys:
    openAI: str = os.getenv('openAI_key')

@dataclass(frozen=True)
class gCloud:
    bucket_name: str = "trash_disposal_app_temporary_pictures_upload"