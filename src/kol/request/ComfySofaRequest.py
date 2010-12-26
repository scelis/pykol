from GenericRequest import GenericRequest
from kol.util import ParseResponseUtils

class ComfySofaRequest(GenericRequest):
    "Uses the comfy sofa in the clan rumpus room."
    def __init__(self, session, numturns):
        super(ComfySofaRequest, self).__init__(session)
        self.url = session.serverURL + "clan_rumpus.php"
        self.requestData['preaction'] = "nap"
        self.requestData['numturns'] = numturns

    def parseResponse(self):
        self.responseData["mp"] = ParseResponseUtils.parseMPGainedLost(self.responseText)
        self.responseData["hp"] = ParseResponseUtils.parseHPGainedLost(self.responseText)
