import os
import time

import requests
def job(get_url: str):
    """Hit a URL until it doesn't give an error, with exponential backoff. """
    print("Running GET job...")
    backoff = int(os.getenv("INITIAL_BACKOFF", 12))
    tries = 4
    while True:
        tries -= 1
        try:
            response = requests.get(get_url)
            print(response.text)
            err = response.status_code >= 400
        except requests.exceptions.ConnectionError as e:
            print(f"Got connection error {e}")
            err = True

        if err:
            if tries <= 0:
                print("Could not complete job. Giving up.")
                break
            print(f"Retrying in {backoff}s...")
            time.sleep(backoff)
            backoff *= 2.0
        else:
            break
    print("done.")

