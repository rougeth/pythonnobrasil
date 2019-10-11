from pythonnobrasil import config
from pythonnobrasil.cal import TomlCalendar


def test_toml_calendar():
    calendar = TomlCalendar(config.CONFERENCIAS_PATH)
    assert calendar
    assert calendar.events
