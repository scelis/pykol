from GenericRequest import GenericRequest

class CharpaneRequest(GenericRequest):
	"Requests the user's character pane."
	
	def __init__(self, session):
		super(CharpaneRequest, self).__init__(session)
		self.url = session.serverURL + 'charpane.php'
