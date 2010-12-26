from GenericRequest import GenericRequest
from kol.manager import PatternManager

class AccountRequest(GenericRequest):
    "Requests the user's account page."
    
    def __init__(self, session):
        super(AccountRequest, self).__init__(session)
        self.url = session.serverURL + "account.php"
        
    def parseResponse(self):
        # Get the user's pwd.
        pwdPattern = PatternManager.getOrCompilePattern('accountPwd')
        pwdMatch = pwdPattern.search(self.responseText)
        self.responseData['pwd'] = pwdMatch.group(1)
        
        # Get the user's ID and name.
        pattern = PatternManager.getOrCompilePattern('accountUserNameAndId')
        match = pattern.search(self.responseText)
        self.responseData['userName'] = match.group(1)
        self.responseData['userId'] = int(match.group(2))
