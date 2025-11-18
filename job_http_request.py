import os
import time

import requests

class JobFailedException(Exception):
    pass

def job_get(url: str):
    print(f"Running GET job to {url}...")
    job(url, "get")


def job_post(url: str):
    print(f"Running POST job to {url}...")
    job(url, "post")


def job(url: str, method: str):
    """Hit a URL until it doesn't give an error, with exponential backoff. """
    backoff = int(os.getenv("INITIAL_RETRY_SECONDS", 12))
    tries = 4
    while True:
        tries -= 1
        try:
            if method == "get":
                response = requests.get(url)
            elif method == "post":
                response = requests.post(url)
            else:
                raise ValueError(f"Unknown operation {method}")
            print(str(response.text)[:300])
            err = response.status_code >= 400
        except requests.exceptions.ConnectionError as e:
            print(f"Got connection error {e}")
            err = True

        if err:
            if tries <= 0:
                print("Could not complete job. Giving up.")
                raise JobFailedException(f"Could not complete job {url}. Giving up.")
            
            print(f"Retrying in {backoff}s...")
            time.sleep(backoff)
            backoff *= 2.0
        else:
            break
    print("done.")

