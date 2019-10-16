import locale
import shutil
from calendar import month_abbr
from datetime import datetime

import ibis

from pythonnobrasil import config, deploy
from pythonnobrasil.cal import GoogleCalendar, TomlCalendar

TODAY = datetime.today()


def prepare_build():
    build_path = str(config.BASE_DIR / 'build')
    static_path = str(config.BASE_DIR / 'static')

    shutil.rmtree(build_path, ignore_errors=True)
    shutil.copytree(static_path, build_path)


def get_template():
    index = config.BASE_DIR / 'static/index.html'
    with index.open() as index_file:
        return ibis.Template(index_file.read())


def get_context(calendar):
    # Set locale to pt_BR so that month_abbr uses Portugues
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

    events = {}
    for month_number in range(1, 13):
        events[month_number] = {
            'abbr': month_abbr[month_number],
            'events': [],
        }

    for event in calendar.events:
        if event.start.year == TODAY.year:
            month = event.start.month
            events[month]['events'].append(event)

    return events


def build_html(calendar):
    context = get_context(calendar)

    template = get_template()
    content = template.render({
        'calendar': context,
        'today': TODAY,
    })

    index = config.BASE_DIR / 'build/index.html'
    with index.open(mode='w') as index_file:
        index_file.write(content)


def create_or_update(local_calendar, google_calendar):
    for event in local_calendar.events:
        gevent = google_calendar.get(event.name)

        if not gevent:
            print('Novo evento: %s' % event.name)
            google_calendar.create_event(event)
            continue

        fields_changed = gevent - event
        if fields_changed:
            print('Atualizando %s: %s' % (event.name, fields_changed))
            google_calendar.update_event(gevent, event)


def main():
    conferencias = config.BASE_DIR.parent / 'conferencias.toml'

    local_calendar = TomlCalendar(conferencias)
    google_calendar = GoogleCalendar()

    create_or_update(local_calendar, google_calendar)

    prepare_build()
    build_html(local_calendar)

    zip = deploy.make_zip('build')
    deploy.push(zip)


if __name__ == '__main__':
    main()
