import requests

def get(url, dest):
    response = requests.get(url)

    if (response.status_code != 200):
        raise ValueError("Non-Success HTTP status (%d) on GET for: '%s'." % (
            response.status_code, url))

    with open(dest, 'wb') as file:
        file.write(response.content)
