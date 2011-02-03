from kol.request.AddPlayerToClanWhitelistRequest import AddPlayerToClanWhitelistRequest
from kol.request.GetClanWhitelistRequest import GetClanWhitelistRequest
from kol.request.LoadClanAdminRequest import LoadClanAdminRequest
from kol.request.ToggleAcceptingClanApplicationsRequest import ToggleAcceptingClanApplicationsRequest

class ClanManager(object):
    "This class can be used as an interface for clan management."

    def __init__(self, session):
        self.session = session
        self.clanName = None
        self.clanCredo = None
        self.clanRanks = None
        self.clanWebsite = None
        self.acceptingApplications = None

    def loadClanAdmin(self):
        r = LoadClanAdminRequest(self.session)
        data = r.doRequest()
        self.clanName = data["clanName"]
        self.clanCredo = data["clanCredo"]
        self.clanWebsite = data["clanWebsite"]
        self.acceptingApplications = data["acceptingApps"]

    def loadClanRanks(self):
        r = GetClanWhitelistRequest(self.session)
        data = r.doRequest()
        self.clanRanks = data["ranks"]

    def setAcceptApplications(self, acceptApplications):
        if self.acceptingApplications == None:
            self.loadClanAdmin()

        if self.acceptingApplications != acceptApplications:
            r = ToggleAcceptingClanApplicationsRequest(self.session)
            r.doRequest()

    def whitelistPlayer(self, player, level, title=""):
        r = AddPlayerToClanWhitelistRequest(self.session, player, level, title)
        r.doRequest()
