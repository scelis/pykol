from GenericRequest import GenericRequest
from kol.util import ParseResponseUtils

class TanULotsRequest(GenericRequest):
	"Uses the Tan-U-Lots Tanning Bed in the clan rumpus room."
	def __init__(self, session):
		super(TanULotsRequest, self).__init__(session)
		self.url = session.serverURL + 'clan_rumpus.php'
		self.requestData['preaction'] = 'gym'
		self.requestData['whichgym'] = '2'
		self.requestData['numturns'] = numTurns
	
	def parseResponse(self):
		self.responseData["substats"] = ParseResponseUtils.parseSubstatsGained(self.responseText, checkMuscle=False, checkMysticality=False)
		self.responseData["stats"] = ParseResponseUtils.ParseResponseUtils.parseStatPointsGained(self.responseText, checkMuscle=False, checkMysticality=False)
		self.responseData["level"] = ParseResponseUtils.parseLevelGained(self.responseText)
