from GenericRequest import GenericRequest

class OpenChatRequest(GenericRequest):
	def __init__(self, session):
		super(OpenChatRequest, self).__init__(session)
		self.url = session.serverURL + "lchat.php"
