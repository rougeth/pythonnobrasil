from collections import defaultdict
from datetime import datetime
import locale
from pathlib import Path
import shutil
from uuid import uuid4

from rcssmin import cssmin

from pythonnobrasil import config
from pythonnobrasil.cal import Calendar
from pythonnobrasil.run import get_template


def get_context(calendar):
    # Set locale to pt_BR so that month_abbr uses Portugues
    locale.setlocale(locale.LC_ALL, "pt_BR.UTF-8")
    context = {}

    events = {
        "next": [],
        "per_year": defaultdict(list),
    }

    now = datetime.today()

    for event in sorted(calendar.events, key=lambda e: e.start, reverse=True):
        if event.start > now.date():
            events["next"].append(event)
        else:
            events["per_year"][event.start.year].append(event)

    events["next"] = sorted(events["next"], key=lambda e: e.start)

    events["per_year"] = {
        year: sorted(events, key=lambda e: e.start)
        for year, events in events["per_year"].items()
    }

    context["events"] = events
    context["updated_at"] = now

    return context


def prepare_build(static_path: Path, build_path: Path):
    shutil.rmtree(build_path, ignore_errors=True)
    shutil.copytree(static_path, build_path)


def minify_static_files(build_path: Path):
    minified_files = []
    build_hash = str(uuid4())[:8]

    for file in build_path.iterdir():
        if file.suffix != ".css":
            continue

        with file.open("r") as fp:
            style = fp.read()
            style_minified = cssmin(style)

        minified_filename = f"{file.stem}.{build_hash}{file.suffix}"
        with open(build_path / minified_filename, mode="w") as fp:
            fp.write(style_minified)
            minified_files.append(
                (file.name, minified_filename),
            )

        file.unlink()

    return minified_files


def build_html(calendar: Calendar, build_path: Path):
    context = get_context(calendar)

    template = get_template()
    content = template.render(**context)

    minified_files = minify_static_files(build_path)
    for filename, minified_filename in minified_files:
        content = content.replace(filename, minified_filename)

    index = build_path / "index.html"
    with index.open(mode="w") as index_file:
        index_file.write(content)
