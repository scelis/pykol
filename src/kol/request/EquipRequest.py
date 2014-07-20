import kol.Error as Error
from GenericRequest import GenericRequest
from kol.manager import PatternManager

class EquipRequest(GenericRequest):
    """
    Equips items from the inventory passed by itemId.  If a slot is specified, it will attempt to equip accessories into that slot.
    """

    def __init__(self, session, itemId, slot=0):
        super(EquipRequest, self).__init__(session)
        self.url = session.serverURL + "inv_equip.php?pwd=" + str(session.pwd) + "&which=2&action=equip&whichitem=" + str(itemId)
        self.requestData["slot"] = slot

    def parseResponse(self):
        "Checks for errors due to equipping items you don't have, or equipping items that aren't equippable."

        noItemPattern = PatternManager.getOrCompilePattern("notEnoughItems")
        match = noItemPattern.search(self.responseText)
        if match:
            raise Error.Error("That item is not in your inventory.", Error.ITEM_NOT_FOUND)

        notEquipmentPattern = PatternManager.getOrCompilePattern("notEquip")
        match = notEquipmentPattern.search(self.responseText)
        if match:
            raise Error.Error("That is not an equippable item.", Error.WRONG_KIND_OF_ITEM)
