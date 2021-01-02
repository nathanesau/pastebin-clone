from config import Config
import time
from datetime import datetime
import requests


def delete_expired_pastes():
    print("Deleting expired pastes at {}".format(datetime.utcnow()))
    try:
        pastes = requests.get(f"{Config.PASTEBIN_API_URL}/pastes/expired").json()["pastes"]
        if not pastes:
            print("No pastes to delete")
        for paste in pastes:
            shortlink = paste["shortlink"]
            print("Deleting expired paste {}".format(shortlink))
            response = requests.delete(f"{Config.PASTEBIN_API_URL}/delete_expired/{shortlink}")
            print("Got response {}".format(response))
    except:
        print("Exception occured trying to delete expired pastes at {}".format(datetime.utcnow()))


if __name__ == "__main__":

    while True:
        delete_expired_pastes()
        time.sleep(60)
