import os
from dotenv import load_dotenv


BASEDIR = os.path.dirname(os.path.realpath(__file__))
load_dotenv(os.path.join(BASEDIR, '.env'))


class Config:
    PASTEBIN_API_URL = os.environ.get('PASTEBIN_API_URL') or \
        "http://localhost:5001/pastebin-clone/api"
