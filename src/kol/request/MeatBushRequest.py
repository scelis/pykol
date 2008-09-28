from kol.request.GenericRequest import GenericRequest
from kol.request import ParseResponseUtils

class MeatBushRequest(GenericRequest):
	"Uses the meat bush in the rumpus room"
	def __init__(self, session):
		super(MeatBushRequest, self).__init__(session)
		self.url = session.serverURL + 'clan_rumpus.php?action=click&spot=4&furni=2'

	def parseResponse(self):
		response = {}
		response["meat"] = ParseResponseUtils.parseMeatReceived(self.responseText)
		
		self.responseData = response
