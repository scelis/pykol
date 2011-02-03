from GenericRequest import GenericRequest
from kol.Error import RequestError, NotEnoughItemsError, InvalidActionError
from kol.manager import PatternManager

class EquipRequest(GenericRequest):
    """
    Equips items from the inventory passed by itemId.  If a slot is specified, it will attempt to equip accessories into that slot.
    """

    def __init__(self, session, itemId, slot=0):
        super(EquipRequest, self).__init__(session)

        self.url = session.serverURL + "inv_equip.php?pwd=" + str(session.pwd) + "&which=2&action=equip&whichitem=" + str(itemId)

        if slot >= 4 or slot < 0:
            raise RequestError("Invalid slot number passed")
        elif slot != 0:
            self.url += "&slot=" + str(slot)

    def parseResponse(self):
        "Checks for errors due to equipping items you don't have, or equipping items that aren't equippable."

        noItemPattern = PatternManager.getOrCompilePattern("notEnoughItems")
        match = noItemPattern.search(self.responseText)
        if match:
            raise NotEnoughItemsError("That item is not in your inventory.")

        notEquipmentPattern = PatternManager.getOrCompilePattern("notEquip")
        match = notEquipmentPattern.search(self.responseText)
        if match:
            raise InvalidActionError("That is not an equippable item.")
