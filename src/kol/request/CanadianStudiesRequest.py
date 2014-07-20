import kol.Error as Error
from GenericRequest import GenericRequest
from kol.manager import PatternManager
from kol.util import ParseResponseUtils

class CanadianStudiesRequest(GenericRequest):
    def __init__(self, session, turns):
        super(CanadianStudiesRequest, self).__init__(session)
        self.url = session.serverURL + "canadia.php"
        self.requestData['action'] = "institute"
        self.requestData['numturns'] = turns

    def parseResponse(self):
        if len(self.responseText) == 0:
            raise Error.Error("You cannot use the Mind Control Device yet.", Error.INVALID_LOCATION)

        noAdventuresPattern = PatternManager.getOrCompilePattern('noAdvInstitue')
        invalidTurnsPattern = PatternManager.getOrCompilePattern('invalidAdvInstitute')
        if noAdventuresPattern.search(self.responseText):
            raise Error.Error("You don't have enough adventures to study at the institute.", Error.NOT_ENOUGH_ADVENTURES)
        if invalidTurnsPattern.search(self.responseText):
            raise Error.Error("That is an invalid number of turns for studying.", Error.REQUEST_GENERIC)

        self.responseData["substats"] = ParseResponseUtils.parseSubstatsGainedLost(self.responseText, checkMuscle=False, checkMoxie=False)
        self.responseData["stats"] = ParseResponseUtils.parseStatsGainedLost(self.responseText, checkMuscle=False, checkMoxie=False)
        self.responseData["level"] = ParseResponseUtils.parseLevelsGained(self.responseText)
