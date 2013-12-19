import kol.Error as Error
from GenericRequest import GenericRequest
from kol.manager import PatternManager

class HomepageRequest(GenericRequest):
    """
    This request is most often used before logging in. It allows the KoL servers to assign a
    particular server number to the user. In addition, it gives us the user's login challenge
    so that we might login to the server in a more secure fashion.
    """

    def __init__(self, session, serverNumber=0):
        super(HomepageRequest, self).__init__(session)
        if serverNumber > 0:
            self.url = "http://www%s.kingdomofloathing.com/main.php" % serverNumber
        else:
            self.url = "http://www.kingdomofloathing.com/"

    def parseResponse(self):
        # Get the URL of the server that we were told to use.
        loginUrlPattern = PatternManager.getOrCompilePattern('loginURL')
        serverMatch = loginUrlPattern.match(self.response.url)
        if serverMatch:
            self.responseData["serverURL"] = serverMatch.group(1)
        else:
            raise Error.Error("Unable to determine server URL from: " + self.response.url, Error.LOGIN_FAILED_GENERIC)

        # Get the user's challenge string which is used to provide a more secure login mechanism.
        loginChallengePattern = PatternManager.getOrCompilePattern('loginChallenge')
        challengeMatch = loginChallengePattern.search(self.responseText)
        if challengeMatch:
            self.responseData["loginChallenge"] = challengeMatch.group(1)
        else:
            raise Error.Error("Unable to find login challenge:\n" + self.responseText, Error.LOGIN_FAILED_GENERIC)
