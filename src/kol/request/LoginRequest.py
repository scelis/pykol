from GenericRequest import GenericRequest
from kol.Error import LoginError, IncorrectPasswordError
from kol.manager import PatternManager

import hashlib

class LoginRequest(GenericRequest):
	def __init__(self, session, loginChallenge):
		super(LoginRequest, self).__init__(session)
		self.url = session.serverURL + "login.php"
		self.requestData['loggingin'] = 'Yup.'
		self.requestData['loginname'] = session.userName
		self.requestData['secure'] = '1'
		hashKey = self.session.userPasswordHash + ":" + loginChallenge
		self.requestData['response'] = hashlib.md5(hashKey).hexdigest()
		self.requestData['challenge'] = loginChallenge
	
	def doRequest(self):
		super(LoginRequest, self).doRequest()
		
		mainFramesetPattern = PatternManager.getOrCompilePattern('mainFrameset')
		if mainFramesetPattern.search(self.responseText):
			self.session.isConnected = True
			return
		
		waitFifteenMinutesPattern = PatternManager.getOrCompilePattern('waitFifteenMinutesLoginError')
		if waitFifteenMinutesPattern.search(self.responseText):
			raise LoginError("Too many login attempts in too short a span of time. Please wait fifteen minutes and try again.", 900)
		
		waitOneMinutePattern = PatternManager.getOrCompilePattern('waitOneMinuteLoginError')
		if waitOneMinutePattern.search(self.responseText):
			raise LoginError("Too many login attempts in too short a span of time. Please wait a minute and try again.", 60)
		
		waitTwoMinutesPattern = PatternManager.getOrCompilePattern('waitTwoMinutesLoginError')
		if waitTwoMinutesPattern.search(self.responseText):
			raise LoginError("Your previous session did not close correctly. Please wait a couple minutes and try again.", 120)
			
		badPasswordPattern = PatternManager.getOrCompilePattern('badPassword')
		if badPasswordPattern.search(self.responseText):
			raise IncorrectPasswordError("Login failed. Bad password.")
			
		tooManyFailuresFromIPPattern = PatternManager.getOrCompilePattern('tooManyLoginsFailuresFromThisIP')
		if tooManyFailuresFromIPPattern.search(self.responseText):
			raise LoginError("Too many login failures from this IP. Please wait 15 minutes and try again.", 900)
			
		raise LoginError("Unknown login error:\n" + self.responseText, 900)
