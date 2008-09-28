from kol.request.GenericRequest import GenericRequest
from kol.request import ParseResponseUtils

class SodaMachineRequest(GenericRequest):
	"Uses the soda machine in the rumpus room"
	def __init__(self, session):
		super(SodaMachineRequest, self).__init__(session)
		self.url = session.serverURL + 'clan_rumpus.php?action=click&spot=3&furni=1'

	def parseResponse(self):
		response = ParseResponseUtils.parseItemsReceived(self.responseText)
		
		self.responseData = response
