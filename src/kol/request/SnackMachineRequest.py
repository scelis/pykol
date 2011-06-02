from kol.request.GenericRequest import GenericRequest
from kol.util import ParseResponseUtils

"""
At the moment, I have no access to a snack machine, so this request only
simulates clicking on it, not selecting a snack.
"""

class SnackMachineRequest(GenericRequest):
    "Uses the Snack Machine in the rumpus room"
    def __init__(self, session):
        super(SnackMachineRequest, self).__init__(session)
        self.url = session.serverURL + 'clan_rumpus.php?action=click&spot=9&furni=2'

    def parseResponse(self):
        items = ParseResponseUtils.parseItemsReceived(self.responseText, self.session)
        self.responseData["items"] = items
