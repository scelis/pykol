from kol.request.GenericRequest import GenericRequest

class DynamicRequest(GenericRequest):
    "A dynamic request to the Kingdom of Loathing servers. Especially useful for a relay browser."
    def __init__(self, session, url, arguments=None):
        super(DynamicRequest, self).__init__(session)
        self.url = session.serverURL + url

        if arguments != None:
            k = arguments.split('&')
            for x in k:
                temp = x.split('=')
                self.requestData[temp[0]] = temp[1]
