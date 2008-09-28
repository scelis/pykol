from kol.request.GenericRequest import GenericRequest
from kol.request import ParseResponseUtils

"""
Currently this requests acts only as a click on the tanning bed.
I do not have access to them, so if more than a simple click is required
I will need info from someone with access to complete this request.
"""

class TanULotsRequest(GenericRequest):
	"Visits the Tan-U-Lots Tanning Bed in the clan rumpus room"
	def __init__(self, session):
		super(TanULotsRequest, self).__init__(session)
		self.url = session.serverURL + 'clan_rumpus.php?action=click&spot=5&furni=2'

	def parseResponse(self):
		response = {}
		respose["substats"] = ParseResponseUtils.parseSubstatsGained(self.responseText, checkMuscle=False, checkMysticality=False)
		respose["statPoints"] = ParseResponseUtils.ParseResponseUtils.parseStatPointsGained(self.responseText, checkMuscle=False, checkMysticality=False)
		response["level"] = ParseResponseUtils.parseLevelGained(self.responseText)
		
		self.responseData = response
