import re
import urllib2
import cherrypy

PATTERN = re.compile(r"<a href=\"image/(.*)\">")
class APODFetcher(object):
    @cherrypy.expose
    def index(self):
        self.image_description = None

        try:
            page = urllib2.urlopen('http://apod.nasa.gov/apod/').read()
        except Exception:
            raise cherrypy.HTTPError(message='Cannot open url')

        image = re.search(PATTERN, page)
        if image is None:
            raise cherrypy.HTTPError(message='Cannot fetch image')

        cherrypy.response.headers['Content-Type']= 'image/jpg'
        url = 'http://apod.nasa.gov/apod/image/' + image.group(1)
        raise cherrypy.HTTPRedirect(url)

    @cherrypy.expose
    def description(self):
        return getattr(self, 'image_description', "Nothing")

if __name__ == '__main__':
    cherrypy.quickstart(APODFetcher(), )