import time

import requests
def job(get_url: str):
    """Hit a URL until it doesn't give an error, with exponential backoff. """
    print("Running GET job...")
    backoff = 6.0
    tries = 4
    while tries > 0:
        tries -= 1
        try:
            response = requests.get(get_url)
            print(response.text)
            err = response.status_code >= 400
        except requests.exceptions.ConnectionError as e:
            print(f"Got connection error {e}")
            err = True

        if err:
            print(f"Retrying in {backoff}s...")
            time.sleep(backoff)
            backoff *= 2.0
        else:
            break

