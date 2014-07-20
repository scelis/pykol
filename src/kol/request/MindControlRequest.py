import kol.Error as Error
from GenericRequest import GenericRequest

class MindControlRequest(GenericRequest):
    def __init__(self, session, level):
        super(MindControlRequest, self).__init__(session)
        self.url = session.serverURL + "canadia.php"
        self.requestData['action'] = "changedial"
        self.requestData['whichlevel'] = level

    def parseResponse(self):
        if len(self.responseText) == 0:
            raise Error.Error("You cannot use the Mind Control Device yet.", Error.INVALID_LOCATION)
