import time
from functools import partial
from http.server import HTTPServer, SimpleHTTPRequestHandler
from multiprocessing import Process
from pathlib import Path

from loguru import logger
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from pythonnobrasil.build import build_html, prepare_build
from pythonnobrasil.cal import TomlCalendar
from pythonnobrasil import config


def start_local_server(port: int, path: Path):
    request_handler = partial(SimpleHTTPRequestHandler, directory=path)
    httpd = HTTPServer(("0.0.0.0", port), request_handler)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.shutdown()


class DevServer(FileSystemEventHandler):
    def __init__(
        self, events_config_file: Path, source_path: Path, build_path: Path, port: int
    ):
        self.server_process = None
        self.server_port = port
        self.build_path = build_path
        self.static_path = str(config.BASE_DIR / "static")
        self.source_path = source_path
        self.events_source_file = events_config_file

    def build(self):
        local_calendar = TomlCalendar(self.events_source_file)
        prepare_build(self.static_path, self.build_path)
        build_html(local_calendar, self.build_path)

    def start_server(self):
        logger.info(f"Starting http local server. port={self.server_port}")
        self.stop_server()

        self.server_process = Process(
            target=start_local_server, args=(self.server_port, self.build_path)
        )
        self.server_process.start()

    def stop_server(self):
        if self.server_process:
            self.server_process.terminate()

    def on_modified(self, event):
        logger.info("File or directory modified, rebuilding website")
        self.build()

    def run(self):
        logger.info(
            f"Running development server. source_path={self.source_path}, build_path={self.build_path}"
        )
        self.build()
        self.start_server()

        observer = Observer()
        observer.schedule(self, self.source_path, recursive=True)
        observer.start()

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()
