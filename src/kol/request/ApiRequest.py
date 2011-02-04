import json
from GenericRequest import GenericRequest
from kol.util import Configuration

class ApiRequest(GenericRequest):
    def __init__(self, session, what="status", **kwargs):
        super(ApiRequest, self).__init__(session)
        self.url = session.serverURL + "api.php"
        self.requestData["what"] = what

        # Create a user agent string.
        userAgent = Configuration.get("applicationName")
        author = Configuration.get("author")
        if author != None and userAgent != None:
            userAgent = "%s+by+%s" % (userAgent, author)
        if userAgent == None:
            userAgent = "pykol+by+Turias"
        self.requestData["for"] = userAgent

        if "count" in kwargs:
            self.requestData["count"] = kwargs["count"]
        if "id" in kwargs:
            self.requestData["id"] = kwargs["id"]
        if "since" in kwargs:
            self.requestData["since"] = kwargs["since"]

    def parseResponse(self):
        self.responseData = json.loads(self.responseText)
