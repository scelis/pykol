from GenericRequest import GenericRequest
from kol.util import ParseResponseUtils

class ArcaneTomesRequest(GenericRequest):
    "Visits the shelf of arcane tomes in the clan rumpus room"
    def __init__(self, session, numTurns):
        super(ArcaneTomesRequest, self).__init__(session)
        self.url = session.serverURL + 'clan_rumpus.php'
        self.requestData['preaction'] = 'gym'
        self.requestData['whichgym'] = '1'
        self.requestData['numturns'] = numTurns

    def parseResponse(self):
        self.responseData["substats"] = ParseResponseUtils.parseSubstatsGainedLost(self.responseText, checkMuscle=False, checkMoxie=False)
        self.responseData["stats"] = ParseResponseUtils.parseStatsGainedLost(self.responseText, checkMuscle=False, checkMoxie=False)
        self.responseData["level"] = ParseResponseUtils.parseLevelsGained(self.responseText)
