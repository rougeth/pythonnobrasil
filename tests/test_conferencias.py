import pytest
import toml


@pytest.fixture
def conferencias():
    filepath = 'conferencias.toml'
    return toml.load(filepath)


def test_toml(conferencias):
    assert conferencias


def test_toml_ordering(conferencias):
    events = conferencias['events']
    events_sorted_by_start = sorted(events, key=lambda d: d['start'])

    assert events == events_sorted_by_start
