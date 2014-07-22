from kol.request.InventoryRequest import InventoryRequest

class InventoryManager(object):
    "This class manages a user's inventory."

    def __init__(self, session):
        "Initializes the InventoryManager with a particular KoL session."
        self.session = session
        session.inventoryManager = self
        self.refreshInventory()

    def refreshInventory(self):
        self.items = {}
        r = InventoryRequest(self.session)
        data = r.doRequest()
        for item in data["items"]:
            self.items[item["id"]] = item["quantity"]
