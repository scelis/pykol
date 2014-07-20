from GenericRequest import GenericRequest
from kol.manager import PatternManager

class LoadClanAdminRequest(GenericRequest):
    "Load's the clan administration page."

    def __init__(self, session):
        super(LoadClanAdminRequest, self).__init__(session)
        self.url = session.serverURL + "clan_admin.php"

    def parseResponse(self):
        # Get the clan name.
        namePattern = PatternManager.getOrCompilePattern("clanName")
        match = namePattern.search(self.responseText)
        self.responseData["clanName"] = match.group(1)

        # Get the clan credo.
        credoPattern = PatternManager.getOrCompilePattern("clanCredo")
        match = credoPattern.search(self.responseText)
        self.responseData["clanCredo"] = match.group(1)

        # Get the clan website.
        websitePattern = PatternManager.getOrCompilePattern("clanWebsite")
        match = websitePattern.search(self.responseText)
        self.responseData["clanWebsite"] = match.group(1)

        # See if the clan is accepting applications.
        clanAcceptingAppsPattern = PatternManager.getOrCompilePattern("clanAcceptingApps")
        if clanAcceptingAppsPattern.search(self.responseText):
            self.responseData["acceptingApps"] = True
        else:
            self.responseData["acceptingApps"] = False
