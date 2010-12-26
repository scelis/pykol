from kol.request.GenericRequest import GenericRequest
from kol.util import ParseResponseUtils

class SodaMachineRequest(GenericRequest):
    "Uses the soda machine in the clan rumpus room."
    def __init__(self, session):
        super(SodaMachineRequest, self).__init__(session)
        self.url = session.serverURL + 'clan_rumpus.php?action=click&spot=3&furni=1'

    def parseResponse(self):
        self.responseData["items"] = ParseResponseUtils.parseItemsReceived(self.responseText, self.session)
