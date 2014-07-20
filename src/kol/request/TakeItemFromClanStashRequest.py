from GenericRequest import GenericRequest

class TakeItemFromClanStashRequest(GenericRequest):
    "Take items from the player's clan stash."

    def __init__(self, session, item):
        super(TakeItemFromClanStashRequest, self).__init__(session)
        self.url = session.serverURL + "clan_stash.php"
        self.requestData["pwd"] = session.pwd
        self.requestData["action"] = "takegoodies"
        self.requestData["whichitem"] = item["id"]
        self.requestData["quantity"] = item["quantity"]

