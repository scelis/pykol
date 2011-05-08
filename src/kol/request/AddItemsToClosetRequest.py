from GenericRequest import GenericRequest

class AddItemsToClosetRequest(GenericRequest):
    "Adds items to the player's closet."

    def __init__(self, session, itemId, quantity="all"):
        super(AddItemsToClosetRequest, self).__init__(session)
        self.url = session.serverURL + "fillcloset.php"
        self.requestData["pwd"] = session.pwd
        self.requestData["action"] = "closetpush"
        self.requestData["whichitem"] = itemId
        self.requestData["qty"] = quantity
        self.requestData["ajax"] = 1
