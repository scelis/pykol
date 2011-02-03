from GenericRequest import GenericRequest
from kol.manager import PatternManager

class OpenChatRequest(GenericRequest):
    def __init__(self, session):
        super(OpenChatRequest, self).__init__(session)
        self.url = session.serverURL + "lchat.php"

    def parseResponse(self):
        currentChannelPattern = PatternManager.getOrCompilePattern("currentChatChannel")
        match = currentChannelPattern.search(self.responseText)
        self.responseData["currentChannel"] = match.group(1)
