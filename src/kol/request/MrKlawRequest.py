from GenericRequest import GenericRequest
from kol.util import ParseResponseUtils

class MrKlawRequest(GenericRequest):
    "Uses Mr. Klaw in the clan rumpus room."
    def __init__(self, session):
        super(MrKlawRequest, self).__init__(session)
        self.url = session.serverURL + 'clan_rumpus.php?action=click&spot=3&furni=3'

    def parseResponse(self):
        self.responseData["items"] = ParseResponseUtils.parseItemsReceived(self.responseText, self.session)
