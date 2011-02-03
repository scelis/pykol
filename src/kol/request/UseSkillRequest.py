from GenericRequest import GenericRequest
from kol.database import SkillDatabase
from kol.manager import PatternManager

class UseSkillRequest(GenericRequest):
    def __init__(self, session, skillId, numTimes=1, targetPlayer=None):
        super(UseSkillRequest, self).__init__(session)
        self.url = session.serverURL + "skills.php"
        self.requestData["pwd"] = session.pwd
        self.requestData["action"] = "Skillz"
        self.requestData["whichskill"] = skillId

        skill = SkillDatabase.getSkillFromId(skillId)
        if skill["type"] == "Buff":
            self.requestData["bufftimes"] = numTimes
            if targetPlayer != None:
                self.requestData["specificplayer"] = targetPlayer
                self.requestData["targetplayer"] = ""
            else:
                self.requestData["specificplayer"] = ""
                self.requestData["targetplayer"] = session.userId
        else:
            self.requestData["quantity"] = numTimes

    def parseResponse(self):
        resultsPattern = PatternManager.getOrCompilePattern('results')
        match = resultsPattern.search(self.responseText)
        if match:
            results = match.group(1)
            self.responseData["results"] = results
