from datetime import datetime
import shutil

from pythonnobrasil import config
from pythonnobrasil.run import get_context, get_template


def prepare_build(build_path=None):
    static_path = str(config.BASE_DIR / 'static')
    if not build_path:
        build_path = str(config.BASE_DIR / 'build')

    shutil.rmtree(build_path, ignore_errors=True)
    shutil.copytree(static_path, build_path)


def build_html(calendar, build_path):
    context = get_context(calendar)

    template = get_template()
    content = template.render({
        'calendar': context,
        'today': datetime.today()
    })

    index = build_path / 'index.html'
    with index.open(mode='w') as index_file:
        index_file.write(content)