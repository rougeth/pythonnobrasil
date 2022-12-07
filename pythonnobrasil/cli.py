import tempfile
from pathlib import Path

import click

from pythonnobrasil import config
from pythonnobrasil.dev import DevServer


@click.group()
def cli():
    ...


@cli.command()
@click.option("--port", type=int, default=3001)
def dev(port):
    conferencias = config.BASE_DIR.parent / "conferencias.toml"
    with tempfile.TemporaryDirectory() as tmp_dirname:
        source_path = config.BASE_DIR.parent
        build_path = Path(tmp_dirname)

        dev_server = DevServer(conferencias, source_path, build_path, port)
        dev_server.run()


if __name__ == "__main__":
    cli()
