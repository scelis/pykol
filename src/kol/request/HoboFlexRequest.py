from kol.request.GenericRequest import GenericRequest
from kol.request import ParseResponseUtils

"""
Currently this requests acts only as a click on the Hobo-Flex.
I do not have access to them, so if more than a simple click is required
I will need info from someone with access to complete this request.
"""

class HoboFlexRequest(GenericRequest):
	"Visits the Hobo-Flex Workout Gym in the clan rumpus room"
	def __init__(self, session):
		super(HoboFlexRequest, self).__init__(session)
		self.url = session.serverURL + 'clan_rumpus.php?action=click&spot=9&furni=1'

	def parseResponse(self):
		response = {}
		respose["substats"] = ParseResponseUtils.parseSubstatsGained(self.responseText, checkMysticality=False, checkMoxie=False)
		respose["statPoints"] = ParseResponseUtils.ParseResponseUtils.parseStatPointsGained(self.responseText, checkMysticality=False, checkMoxie=False)
		response["level"] = ParseResponseUtils.parseLevelGained(self.responseText)
		
		self.responseData = response
