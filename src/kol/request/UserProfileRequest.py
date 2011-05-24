from GenericRequest import GenericRequest
from kol.manager import PatternManager

class UserProfileRequest(GenericRequest):
    def __init__(self, session, playerId):
        super(UserProfileRequest, self).__init__(session)
        self.url = session.serverURL + "showplayer.php"
        self.requestData["who"] = playerId
    
    def parseResponse(self):
        usernamePattern = PatternManager.getOrCompilePattern('profileUserName')
        match = usernamePattern.search(self.responseText)
        self.responseData["userName"] = match.group(1)
