from ApiRequest import ApiRequest

class StatusRequest(ApiRequest):
    def __init__(self, session):
        super(StatusRequest, self).__init__(session)
        self.url = session.serverURL + "api.php"
        self.requestData["what"] = "status"
    
    def parseResponse(self):
        super(StatusRequest, self).parseResponse()
        self.responseData = self.jsonData
