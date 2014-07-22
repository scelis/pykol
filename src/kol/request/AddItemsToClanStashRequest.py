from GenericRequest import GenericRequest

class AddItemsToClanStashRequest(GenericRequest):
    "Adds items to the player's clan stash."

    def __init__(self, session, items):
        super(AddItemsToClanStashRequest, self).__init__(session)
        self.url = session.serverURL + "clan_stash.php"
        self.requestData["pwd"] = session.pwd
        self.requestData["action"] = "addgoodies"

        ctr = 0
        for item in items:
            ctr += 1
            self.requestData["item%s" % ctr] = item["id"]
            self.requestData["qty%s" % ctr] = item["quantity"]
