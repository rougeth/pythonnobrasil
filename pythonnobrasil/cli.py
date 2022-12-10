import os
import tempfile
from pathlib import Path

import click

from pythonnobrasil import config
from pythonnobrasil.build import build_html, prepare_build
from pythonnobrasil.cal import GoogleCalendar, TomlCalendar
from pythonnobrasil.dev import DevServer
from pythonnobrasil.run import create_or_update


@click.group()
def cli():
    ...


@cli.command()
@click.option(
    "--output",
    type=click.Path(exists=True, file_okay=False, path_type=Path),
    default=config.BASE_DIR / "output",
)
def deploy(output):
    conferencias = config.BASE_DIR.parent / "conferencias.toml"
    static_path = config.BASE_DIR / "static"
    build_path = config.BASE_DIR / "static"
    local_calendar = TomlCalendar(conferencias)

    google_calendar = GoogleCalendar(conferencias)
    create_or_update(local_calendar, google_calendar)

    prepare_build(static_path, output)
    build_html(local_calendar, output)


@cli.command()
@click.option("--update-external-calendar", is_flag=True)
@click.option(
    "--output",
    type=click.Path(file_okay=False, path_type=Path),
    default=config.BASE_DIR / "output",
)
def build(output: Path, update_external_calendar: bool):
    if not output.exists():
        os.mkdir(output)

    conferencias = config.BASE_DIR.parent / "conferencias.toml"
    static_path = config.BASE_DIR / "static"
    local_calendar = TomlCalendar(conferencias)

    if update_external_calendar:
        google_calendar = GoogleCalendar()
        create_or_update(local_calendar, google_calendar)

    prepare_build(static_path, output)
    build_html(local_calendar, output)


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
