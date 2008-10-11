from GenericRequest import GenericRequest
from kol.manager import PatternManager
from kol.util import ParseResponseUtils
from kol.Error import UserShouldNotBeHereError, NotEnoughAdventuresLeftError, RequestError

class CanadianStudiesRequest(GenericRequest):
	def __init__(self, session, turns):
		super(CanadianStudiesRequest, self).__init__(session)
		self.url = session.serverURL + "canadia.php"
		self.requestData['action'] = "institute"
		self.requestData['numturns'] = turns

	def parseResponse(self):
		if len(self.responseText) == 0:
			raise UserShouldNotBeHereError("You cannot use the Mind Control Device yet.")
		
		NoAdventuresPattern = PatternManager.getOrCompilePattern('noAdvInstitue')
		InvalidTurnsPattern = PatternManager.getOrCompilePattern('invalidAdvInstitute')
		
		if NoAdventuresPattern.search(self.responseText):
			raise NotEnoughAdventuresLeftError("You don't have enough adventures to study at the institute.")
		if InvalidTurnsPattern.search(self.responseText):
			raise RequestError("That is an invalid number of turns for studying")
		
		self.responseData["substats"] = ParseResponseUtils.parseSubstatsGainedLost(self.responseText, checkMuscle=False, checkMoxie=False)
		self.responseData["stats"] = ParseResponseUtils.ParseResponseUtils.parseStatsGainedLost(self.responseText, checkMuscle=False, checkMoxie=False)
		self.responseData["level"] = ParseResponseUtils.parseLevelsGained(self.responseText)
