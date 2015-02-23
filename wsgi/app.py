import os
import re
import urllib2

from bottle import route, abort, redirect, run, default_app


PATTERN = re.compile(r"<a href=\"image/(.*)\">")

application = default_app()


@route('/')
def index():
    try:
        page = urllib2.urlopen('http://apod.nasa.gov/apod/').read()
    except Exception as e:
        raise abort(500, 'Cannot open url.\n' + str(e))

    image = re.search(PATTERN, page)
    if image is None:
        raise abort(500, 'Cannot fetch image')

    url = 'http://apod.nasa.gov/apod/image/' + image.group(1)
    raise redirect(url)


if __name__ == '__main__':
    run(host='localhost', port=8080)
