from GenericRequest import GenericRequest

class AddMeatToClosetRequest(GenericRequest):
    "Adds meat to the player's closet."

    def __init__(self, session, meat=""):
        super(AddMeatToClosetRequest, self).__init__(session)
        self.url = session.serverURL + "closet.php"
        self.requestData["pwd"] = session.pwd
        self.requestData["action"] = "addmeat"
        self.requestData["amt"] = meat
