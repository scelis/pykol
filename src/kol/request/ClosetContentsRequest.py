from GenericRequest import GenericRequest

class ClosetContentsRequest(GenericRequest):
	def __init__(self, session):
		super(ClosetContentsRequest, self).__init__(session)
		self.url = session.serverURL + "closet.php"
