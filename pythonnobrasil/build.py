from datetime import datetime
from pathlib import Path
import shutil

from pythonnobrasil import config
from pythonnobrasil.cal import Calendar
from pythonnobrasil.run import get_context, get_template


def prepare_build(static_path: Path, build_path: Path):
    shutil.rmtree(build_path, ignore_errors=True)
    shutil.copytree(static_path, build_path)


def build_html(calendar: Calendar, build_path: Path):
    context = get_context(calendar)

    template = get_template()
    content = template.render({"calendar": context, "today": datetime.today()})

    index = build_path / "index.html"
    with index.open(mode="w") as index_file:
        index_file.write(content)
