import cookielib
import urllib2
import urllib

try:
    import requests
except ImportError:
    requests = None


class Response(object):
    "This class abstracts handling request responses created by an opener"

    def __init__(self, text, url):
        self.text = text
        self.url = url

class StandardOpener(object):
    "This class provides a generic wrapper around urllib2 stuff"

    def __init__(self):
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookielib.CookieJar()))

    def open(self, url, requestData):
        self.response = self.opener.open(url, urllib.urlencode(requestData))
        return Response(self.response.read(), self.response.geturl())

class RequestsOpener(object):
    "This class provides a generic wrapper around requests"

    def __init__(self):
        self.opener = requests.Session()

    def open(self, url, requestData):
        self.response = self.opener.post(url, data = requestData)
        return Response(self.response.text, self.response.url)
