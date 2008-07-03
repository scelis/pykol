from GenericRequest import GenericRequest
from kol.manager import PatternManager

class AccountRequest(GenericRequest):
	"""
	Requests the user's account page. Right now it is really only useful for obtaining both the
	user's ID as well as the user's generated pwd for the session.
	"""
	
	def __init__(self, session):
		super(AccountRequest, self).__init__(session)
		self.url = session.serverURL + "account.php"
		
	def getPwd(self):
		"Returns the user's pwd."
		pwdPattern = PatternManager.getOrCompilePattern('accountPwd')
		pwdMatch = pwdPattern.search(self.responseText)
		return pwdMatch.group(1)
		
	def getUserId(self):
		"Returns the user's ID."
		pattern = PatternManager.getOrCompilePattern('accountUserNameAndId')
		match = pattern.search(self.responseText)
		return int(match.group(2))
	
	def getUserName(self):
		"Returns the user's name."
		pattern = PatternManager.getOrCompilePattern('accountUserNameAndId')
		match = pattern.search(self.responseText)
		return match.group(1)
