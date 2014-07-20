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

        playerClanPattern = PatternManager.getOrCompilePattern('profileClan')
        match = playerClanPattern.search(self.responseText)
        if match:
            self.responseData["clanId"] = int(match.group(1))
            self.responseData["clanName"] = match.group(2)

        numberAscensionsPattern = PatternManager.getOrCompilePattern('profileNumAscensions')
        match = numberAscensionsPattern.search(self.responseText)
        if match:
            self.responseData["numAscensions"] = int(match.group(1))
        else:
            self.responseData["numAscensions"] = 0

        numberTrophiesPattern = PatternManager.getOrCompilePattern('profileNumTrophies')
        match = numberTrophiesPattern.search(self.responseText)
        if match:
            self.responseData["numTrophies"] = int(match.group(1))
        else:
            self.responseData["numTrophies"] = 0

        numberTattoosPattern = PatternManager.getOrCompilePattern('profileNumTattoos')
        match = numberTattoosPattern.search(self.responseText)
        if match:
            self.responseData["numTattoos"] = int(match.group(1))
        else:
            self.responseData["numTattoos"] = 0
