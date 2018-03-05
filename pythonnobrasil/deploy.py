import io
import os
from pathlib import Path
from zipfile import ZipFile

import requests

import config


def make_zip(path):
    build_folder = Path(path)
    filenames = [f for f in build_folder.iterdir() if not f.name.startswith('.')]

    buffer = io.BytesIO()
    with ZipFile(buffer, 'w') as _zip:
        for filename in filenames:
            _zip.write(str(filename))

    buffer.seek(0)
    return buffer


def push(zip):
    headers = {
        'Content-Type': 'application/zip',
    }
    params = {
        'access_token': config.NETLIFY_TOKEN,
    }

    url = '{}/sites/{}/deploys'.format(config.NETLIFY_API,
                                       config.NETLIFY_SITE_ID)
    response = requests.post(url, data=zip, headers=headers, params=params)
