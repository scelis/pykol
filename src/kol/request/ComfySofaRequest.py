from kol.request.GenericRequest import GenericRequest
from kol.util import CommonPatternUtils

class ComfySofaRequest(GenericRequest):
	"Uses the comfy sofa in the rumpus room"
	def __init__(self, session, numturns=1):
		super(ComfySofaRequest, self).__init__(session)
		self.url = session.serverURL + "clan_rumpus.php"
		self.requestData['preaction'] = "nap"
		self.requestData['numturns'] = numturns

	def parseResponse(self):
		response = CommonPatternUtils.checkText(self.responseText, check=[ CommonPatternUtils.HEALTH])
		
		self.responseData = response
