import kol.Error as Error
from GenericRequest import GenericRequest
from kol.util import Configuration

import json

class ApiRequest(GenericRequest):
    def __init__(self, session):
        super(ApiRequest, self).__init__(session)
        self.url = session.serverURL + "api.php"

        # Create a user agent string.
        userAgent = Configuration.get("userAgent")
        if userAgent == None:
            userAgent = "pykol+by+Turias"
        self.requestData["for"] = userAgent
    
    def parseResponse(self):
        self.jsonData = json.loads(self.responseText)
        if type(self.jsonData) == str or type(self.jsonData) == unicode:
            raise Error.Error(self.jsonData, Error.REQUEST_GENERIC)
