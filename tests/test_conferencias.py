import yaml


def test_yaml():
    with open('conferencias.yaml') as file:
        confs = yaml.load(file, Loader=yaml.SafeLoader)
    assert confs
