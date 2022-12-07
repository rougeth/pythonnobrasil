from functools import partial
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path


def run_dev_server(build_path: Path, port: int):
    request_handler = partial(SimpleHTTPRequestHandler, directory=build_path)
    httpd = HTTPServer(("0.0.0.0", port), request_handler)
    httpd.serve_forever()