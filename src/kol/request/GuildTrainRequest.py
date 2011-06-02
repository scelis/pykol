from GenericRequest import GenericRequest
from kol.manager import PatternManager
from kol.database import SkillDatabase
import kol.Error as Error

class GuildTrainRequest(GenericRequest):
    def __init__(self, session, skillId):
        super(GuildTrainRequest, self).__init__(session)
        self.url = session.serverURL + "guild.php"
        self.requestData["pwd"] = session.pwd
        self.requestData["action"] = "train"
        self.requestData["whichskill"] = skillId

    def parseResponse(self):
        weakSkillPattern = PatternManager.getOrCompilePattern('skillTooWeak')
        badSkillPattern = PatternManager.getOrCompilePattern('skillNotTrainable')
        poorSkillPattern = PatternManager.getOrCompilePattern('skillTooPoor')
        haveSkillPattern = PatternManager.getOrCompilePattern('skillHaveAlready')

        if weakSkillPattern.search(self.responseText):
            raise Error.Error("You aren't a high enough level to train that skill.", Error.USER_IS_LOW_LEVEL)
        if badSkillPattern.search(self.responseText):
            raise Error.Error("You cannot train that skill at the Guild Hall.", Error.SKILL_NOT_FOUND)
        if poorSkillPattern.search(self.responseText):
            raise Error.Error("You cannot afford to train that skill", Error.NOT_ENOUGH_MEAT)
        if haveSkillPattern.search(self.responseText):
            raise Error.Error("You already know that skill.", Error.ALREADY_COMPLETED)

        skillLearnedPattern = PatternManager.getOrCompilePattern('skillLearned')
        match = skillLearnedPattern.search(self.responseText)
        skill = SkillDatabase.getSkillFromName(match.group(1))
        self.responseData["skill"] = skill
