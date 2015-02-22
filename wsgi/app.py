import os
import re
import urllib2

from bottle import route, abort, redirect, run, default_app, TEMPLATE_PATH


TEMPLATE_PATH.append(os.path.join(os.environ['OPENSHIFT_REPO_DIR'], 'wsgi/views/'))

PATTERN = re.compile(r"<a href=\"image/(.*)\">")

application = default_app()


@route('/')
def index():
    try:
        page = urllib2.urlopen('http://apod.nasa.gov/apod/').read()
    except Exception:
        raise abort(500, 'Cannot open url')

    image = re.search(PATTERN, page)
    if image is None:
        raise abort(500, 'Cannot fetch image')

    url = 'http://apod.nasa.gov/apod/image/' + image.group(1)
    raise redirect(url)


if __name__ == '__main__':
    run(host='localhost', port=8080)