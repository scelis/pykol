from kol.request.GenericRequest import GenericRequest
from kol.request import ParseResponseUtils

class OldTimeyRadioRequest(GenericRequest):
	"Uses the Old-Timey Radio in the rumpus room"
	def __init__(self, session):
		super(OldTimeyRadioRequest, self).__init__(session)
		self.url = session.serverURL + 'clan_rumpus.php?action=click&spot=4&furni=1'

	def parseResponse(self):
		response = ParseResponseUtils.parseEffectsGained(self.responseText)
		
		self.responseData = response
