from datetime import datetime
from pathlib import Path
from unittest.mock import patch
from pythonnobrasil.build import minify_static_files, prepare_build, build_html
from pythonnobrasil import config
from pythonnobrasil.cal import Calendar, Event


def test_prepare_build(tmp_path: Path):
    old_file = tmp_path / "old-file"
    old_file.open(mode="w").close()
    static_path = config.BASE_DIR / "static"

    prepare_build(static_path, tmp_path)

    files = list(tmp_path.iterdir())
    assert old_file not in files
    assert len(files) == 3


def test_build_html(tmp_path: Path):
    today = datetime.now().date()
    static_path = config.BASE_DIR / "static"
    prepare_build(static_path, tmp_path)

    event = Event("Python Brasil 3000", today, today, "Future", "https://localhost")
    calendar = Calendar()
    calendar.events = [event]

    build_html(calendar, tmp_path)

    files = list(tmp_path.iterdir())
    assert len(files) == 3
    assert event.name in files[0].open().read()


@patch("pythonnobrasil.build.uuid4")
def test_minify_static_files(uuid4_mock, tmp_path: Path):
    uuid4_mock.return_value = "1234567890"
    static_path = config.BASE_DIR / "static"
    prepare_build(static_path, tmp_path)

    minified_files = minify_static_files(tmp_path)

    css_filename = "style.css"
    minified_css_filename = f"style.{uuid4_mock.return_value[:8]}.css"
    assert minified_files == [
        (css_filename, minified_css_filename),
    ]
    assert not (tmp_path / css_filename).exists()
    assert (tmp_path / minified_css_filename).exists()
