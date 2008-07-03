from GenericRequest import GenericRequest

class LogoutRequest(GenericRequest):
	def __init__(self, session):
		super(LogoutRequest, self).__init__(session)
		self.url = session.serverURL + "logout.php"

	def doRequest(self):
		super(LogoutRequest, self).doRequest()
		self.session.isConnected = False
