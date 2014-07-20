import kol.Error as Error
from GenericRequest import GenericRequest
from kol.manager import PatternManager

import hashlib

class LoginRequest(GenericRequest):
    """
    A request to login to The Kingdom of Loathing. This class will look for various login
    errors. If any occur, than an appropriate exception is raised.
    """

    def __init__(self, session, loginChallenge):
        super(LoginRequest, self).__init__(session)
        self.url = session.serverURL + "login.php"
        self.requestData['loggingin'] = 'Yup.'
        self.requestData['loginname'] = session.userName
        self.requestData['secure'] = '1'
        hashKey = self.session.userPasswordHash + ":" + loginChallenge
        self.requestData['response'] = hashlib.md5(hashKey).hexdigest()
        self.requestData['challenge'] = loginChallenge

    def parseResponse(self):
        mainFramesetPattern = PatternManager.getOrCompilePattern('mainFrameset')
        if mainFramesetPattern.search(self.responseText):
            self.session.isConnected = True
            return

        waitFifteenMinutesPattern = PatternManager.getOrCompilePattern('waitFifteenMinutesLoginError')
        if waitFifteenMinutesPattern.search(self.responseText):
            e = Error.Error("Too many login attempts in too short a span of time. Please wait fifteen minutes and try again.", Error.LOGIN_FAILED_GENERIC)
            e.timeToWait = 900
            raise e

        waitFiveMinutesPattern = PatternManager.getOrCompilePattern('waitFiveMinutesLoginError')
        if waitFiveMinutesPattern.search(self.responseText):
            e = Error.Error("Too many login attempts in too short a span of time. Please wait five minutes and try again.", Error.LOGIN_FAILED_GENERIC)
            e.timeToWait = 300
            raise e

        waitOneMinutePattern = PatternManager.getOrCompilePattern('waitOneMinuteLoginError')
        if waitOneMinutePattern.search(self.responseText):
            e = Error.Error("Too many login attempts in too short a span of time. Please wait a minute and try again.", Error.LOGIN_FAILED_GENERIC)
            e.timeToWait = 60
            raise e

        waitTwoMinutesPattern = PatternManager.getOrCompilePattern('waitTwoMinutesLoginError')
        if waitTwoMinutesPattern.search(self.responseText):
            e = Error.Error("Your previous session did not close correctly. Please wait a couple of minutes and try again.", Error.LOGIN_FAILED_GENERIC)
            e.timeToWait = 120
            raise e

        badPasswordPattern = PatternManager.getOrCompilePattern('badPassword')
        if badPasswordPattern.search(self.responseText):
            raise Error.Error("Login failed. Bad password.", Error.LOGIN_FAILED_BAD_PASSWORD)

        tooManyFailuresFromIPPattern = PatternManager.getOrCompilePattern('tooManyLoginsFailuresFromThisIP')
        if tooManyFailuresFromIPPattern.search(self.responseText):
            e = Error.Error("Too many login failures from this IP. Please wait 15 minutes and try again.", Error.LOGIN_FAILED_GENERIC)
            e.timeToWait = 900
            raise e

        e = Error.Error("Unknown login error.", Error.LOGIN_FAILED_GENERIC)
        e.timeToWait = 900
        raise e
