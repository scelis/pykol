from GenericRequest import GenericRequest
from kol.util import ParseResponseUtils

class MeatBushRequest(GenericRequest):
    "Uses the meat bush in the clan rumpus room."
    def __init__(self, session):
        super(MeatBushRequest, self).__init__(session)
        self.url = session.serverURL + 'clan_rumpus.php?action=click&spot=4&furni=2'

    def parseResponse(self):
        self.responseData["meat"] = ParseResponseUtils.parseMeatGainedLost(self.responseText)
