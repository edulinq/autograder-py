import shutil
import requests

def get(url, dest):
    # Use stream = True to avoid loading the entire response into memory.
    with requests.get(url, stream = True) as response:
        if (response.status_code != 200):
            raise ValueError("Non-Success HTTP status (%d) on GET for: '%s'." % (
                response.status_code, url))

        with open(dest, 'wb') as file:
            shutil.copyfileobj(response.raw, file)
