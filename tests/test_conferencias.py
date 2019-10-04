import toml


def test_toml():
    filepath = 'conferencias.toml'
    confs = toml.load(filepath)
    assert confs
