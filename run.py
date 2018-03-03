import shutil
import locale
from calendar import month_abbr

import ibis

import deploy
from cal import GoogleCalendar, YamlCalendar



def prepare_build():
    shutil.rmtree('./build', ignore_errors=True)
    shutil.copytree('./static', './build')


def get_template():
    with open('static/index.html') as index_file:
        return ibis.Template(index_file.read())


def get_context(calendar):
    # Set locale to pt_BR so that month_abbr uses Portugues
    locale.setlocale(locale.LC_ALL, 'pt_BR')

    events = {}
    for month_number in range(1, 13):
        events[month_number] = {
            'abbr': month_abbr[month_number],
            'events': [],
        }

    for event in calendar.events:
        month = event.start.month
        events[month]['events'].append(event)

    return events


def build_html(calendar):
    context = get_context(calendar)

    template = get_template()
    content = template.render({'calendar': context})

    with open('build/index.html', 'w') as index_file:
        index_file.write(content)


def create_or_update(local_calendar, google_calendar):
    for event in local_calendar.events:
        gevent = google_calendar.get(event.name)

        if not gevent:
            google_calendar.create_event(event)
            continue

        need_update = gevent - event
        if need_update:
            print('need to update: %s' % need_update)
            google_calendar.update_event(gevent, event)


def main():
    local_calendar = YamlCalendar('conferences.yaml')
    google_calendar = GoogleCalendar()

    create_or_update(local_calendar, google_calendar)

    prepare_build()
    build_html(local_calendar)

    zip = deploy.make_zip('build')
    deploy.push(zip)


if __name__ == '__main__':
    main()
