from kol.request.GenericRequest import GenericRequest
from kol.util import ParseResponseUtils

"""
At the moment, I have no access to a jukebox, so this request only simulates clicking on the jukebox, not selecting a song.
"""
class JukeboxRequest(GenericRequest):
    "Uses the jukebox in the rumpus room"
    def __init__(self, session, whichsong):
        super(JukeboxRequest, self).__init__(session)
        self.url = session.serverURL + 'clan_rumpus.php?action=click&spot=3&furni=2'

    def parseResponse(self):
        response = {}
        effectResponse = ParseResponseUtils.parseEffectsGained(self.responseText)
        if len(effectResponse) > 0:
            response["effects"] = effectResponse
        hpResponse = ParseResponseUtils.parseHPGainedLost(self.responseText)
        if hpResponse != 0:
            response["hp"] = hpResponse

        self.responseData = response
