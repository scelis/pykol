from GenericRequest import GenericRequest
from kol.util import ParseResponseUtils

class OldTimeyRadioRequest(GenericRequest):
    "Uses the Old-Timey Radio in the clan rumpus room."
    def __init__(self, session):
        super(OldTimeyRadioRequest, self).__init__(session)
        self.url = session.serverURL + 'clan_rumpus.php?action=click&spot=4&furni=1'

    def parseResponse(self):
        self.responseData["effects"] = ParseResponseUtils.parseEffectsGained(self.responseText)
