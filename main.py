import re
import urllib2
from bottle import route, abort, redirect, run


PATTERN = \
    re.compile(r"<a href=\"image/(.*)\">")

DESCRIPTION = None


@route('/')
def index():
    DESCRIPTION = None

    try:
        page = urllib2.urlopen('http://apod.nasa.gov/apod/').read()
    except Exception:
        raise abort(500, 'Cannot open url')

    image = re.search(PATTERN, page)
    if image is None:
        raise abort(500, 'Cannot fetch image')

    url = 'http://apod.nasa.gov/apod/image/' + image.group(1)
    raise redirect(url)


@route('/description')
def description():
    return DESCRIPTION or "Nothing"


if __name__ == '__main__':
    run(host='localhost', port=8080)