from GenericRequest import GenericRequest

class TakeMeatFromClosetRequest(GenericRequest):
    "Adds meat to the player's closet."

    def __init__(self, session, meat=""):
        super(TakeMeatFromClosetRequest, self).__init__(session)
        self.url = session.serverURL + "closet.php"
        self.requestData["pwd"] = session.pwd
        self.requestData["action"] = "takemeat"
        self.requestData["amt"] = meat
