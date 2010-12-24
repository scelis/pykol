from GenericRequest import GenericRequest

class AddPlayerToClanWhitelistRequest(GenericRequest):
    def __init__(self, session, player, level, title=""):
        super(AddPlayerToClanWhitelistRequest, self).__init__(session)
        self.url = session.serverURL + "clan_whitelist.php"
        self.requestData["action"] = "add"
        self.requestData["pwd"] = session.pwd
        self.requestData["addwho"] = player
        self.requestData["level"] = level
        self.requestData["title"] = title
