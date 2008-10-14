from GenericRequest import GenericRequest
from kol.util import Report
from kol.manager import PatternManager
from kol.database import SkillDatabase
from kol.Error import SkillMissingError, NotEnoughMeatError, InvalidActionError, SkillNotFoundError, RequestError

class GuildTrainRequest(GenericRequest):
	def __init__(self, session, skillId):
		super(GuildTrainRequest, self).__init__(session)
		self.url = session.serverURL + "guild.php"
		self.requestData["pwd"] = session.pwd
		self.requestData["action"] = "train"
		self.requestData["whichskill"] = skillId%1000
	
	def parseResponse(self):
		weakSkillPattern = PatternManager.getOrCompilePattern('skillTooWeak')
		badSkillPattern = PatternManager.getOrCompilePattern('skillNotTrainable')
		poorSkillPattern = PatternManager.getOrCompilePattern('skillTooPoor')
		haveSkillPattern = PatternManager.getOrCompilePattern('skillHaveAlready')
		
		if weakSkillPattern.search(self.responseText):
			raise InvalidActionError("You aren't a high enough level to train that skill")
		if badSkillPattern.search(self.responseText):
			raise SkillMissingError("You cannot train that skill at the Guild Hall")
		if poorSkillPattern.search(self.responseText):
			raise NotEnoughMeatError("You cannot afford to train that skill")
		if haveSkillPattern.search(self.responseText):
			raise RequestError("You already know that skill")
		
		skillLearnedPattern = PatternManager.getOrCompilePattern('skillLearned')
		match = skillLearnedPattern.search(self.responseText)
		if match:
			try:
				skill = SkillDatabase.getSkillFromName(match.group(1))
				self.responseData["skill"] = skill
			except SkillNotFoundError, inst:
				Report.error("bot", inst.message, inst)
