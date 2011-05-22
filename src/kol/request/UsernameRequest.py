from GenericRequest import GenericRequest
from kol.manager import PatternManager

class UsernameRequest(GenericRequest):
    def __init__(self, session, playerId):
        super(UsernameRequest, self).__init__(session)
        self.url = session.serverURL + "showplayer.php?who=%s" % playerId
    
    def parseResponse(self):
        """
        Parses through the response and simply returns the username
        of the player.
        """
        
        usernamePattern = PatternManager.getOrCompilePattern('username')
        
        stripText = self.responseText.replace('\n','')
        
        for username in usernamePattern.finditer(stripText):
            name = username.group(1).lower()
            if name == 'sorry...':
                self.responseData = ''
            else:
                self.responseData = name