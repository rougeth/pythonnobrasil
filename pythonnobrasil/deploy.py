import io
from zipfile import ZipFile

import requests

from pythonnobrasil import config

NETLIFY_API = "https://api.netlify.com/api/v1"


def make_zip(path):
    build_folder = config.BASE_DIR / path
    filenames = [f for f in build_folder.iterdir() if not f.name.startswith(".")]

    buffer = io.BytesIO()
    with ZipFile(buffer, "w") as _zip:
        for filename in filenames:
            _zip.write(str(filename))

    buffer.seek(0)
    return buffer


def push(zip):
    headers = {
        "Content-Type": "application/zip",
    }
    params = {
        "access_token": config.NETLIFY_TOKEN,
    }

    url = "{}/sites/{}/deploys".format(NETLIFY_API, config.NETLIFY_SITE_ID)
    response = requests.post(url, data=zip, headers=headers, params=params)

    error = response.json()["error_message"]
    if error:
        print(error)
