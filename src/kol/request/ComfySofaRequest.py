from kol.request.GenericRequest import GenericRequest
from kol.request import ParseResponseUtils

class ComfySofaRequest(GenericRequest):
	"Uses the comfy sofa in the rumpus room"
	def __init__(self, session, numturns=1):
		super(ComfySofaRequest, self).__init__(session)
		self.url = session.serverURL + "clan_rumpus.php"
		self.requestData['preaction'] = "nap"
		self.requestData['numturns'] = numturns

	def parseResponse(self):
		response = {}
		response["mp"] = ParseResponseUtils.parseMPGained(self.responseText)
		response["hp"] = ParseResponseUtils.parseHPGained(self.responseText)
		
		self.responseData = response
