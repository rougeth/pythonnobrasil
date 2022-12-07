import tempfile
from pathlib import Path

import click

from pythonnobrasil import config
from pythonnobrasil.build import build_html, prepare_build
from pythonnobrasil.cal import TomlCalendar
from pythonnobrasil.dev import run_dev_server


@click.group()
def cli():
    ...


@cli.command()
@click.option("--port", type=int, default=3001)
def dev(port):
    conferencias = config.BASE_DIR.parent / "conferencias.toml"
    local_calendar = TomlCalendar(conferencias)
    with tempfile.TemporaryDirectory() as tmp_dirname:
        build_path = Path(tmp_dirname)
        prepare_build(build_path)
        build_html(local_calendar, build_path)
        run_dev_server(build_path, port)


if __name__ == "__main__":
    cli()
