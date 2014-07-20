from GenericRequest import GenericRequest
from kol.manager import PatternManager
from kol.database import ItemDatabase

class CurrentEquipmentRequest(GenericRequest):
    """
    Gets info on all equipment currently equipped.
    Returns a lookup from the item database for each item equipped.
    For accessories, two possibilities are present.  If equipping each slot seperately is enabled, each item's dictionary will contain an attribute "slot" with the number of the slot it occupies.  Otherwise, the "slot" attribute will have the value 0 for all equipped accessories.
    """

    def __init__(self, session):
        super(CurrentEquipmentRequest, self).__init__(session)
        self.session = session
        self.url = session.serverURL + "inventory.php?which=2"

    def parseResponse(self):
        hatPattern = PatternManager.getOrCompilePattern("currentHat")
        weaponPattern = PatternManager.getOrCompilePattern("currentWeapon")
        offhandPattern = PatternManager.getOrCompilePattern("currentOffhand")
        shirtPattern = PatternManager.getOrCompilePattern("currentShirt")
        pantsPattern = PatternManager.getOrCompilePattern("currentPants")
        accPattern = PatternManager.getOrCompilePattern("currentAcc")
        acc1Pattern = PatternManager.getOrCompilePattern("currentAcc1")
        acc2Pattern = PatternManager.getOrCompilePattern("currentAcc2")
        acc3Pattern = PatternManager.getOrCompilePattern("currentAcc3")
        familiarPattern = PatternManager.getOrCompilePattern("currentFam")

        hatText = hatPattern.search(self.responseText)
        if hatText:
            self.responseData["hat"] = ItemDatabase.getOrDiscoverItemFromDescId(int(hatText.group(1)), self.session)

        weaponText = weaponPattern.search(self.responseText)
        if weaponText:
            self.responseData["weapon"] = ItemDatabase.getOrDiscoverItemFromDescId(int(weaponText.group(1)), self.session)

        offhandText = offhandPattern.search(self.responseText)
        if offhandText:
            self.responseData["offhand"] = ItemDatabase.getOrDiscoverItemFromDescId(int(offhandText.group(1)), self.session)

        shirtText = shirtPattern.search(self.responseText)
        if shirtText:
            self.responseData["shirt"] = ItemDatabase.getOrDiscoverItemFromDescId(int(shirtText.group(1)), self.session)

        pantsText = pantsPattern.search(self.responseText)
        if pantsText:
            self.responseData["pants"] = ItemDatabase.getOrDiscoverItemFromDescId(int(pantsText.group(1)), self.session)

        accessories = []
        accText = accPattern.search(self.responseText)
        if accText:
            for match in accPattern.finditer(self.responseText):
                item = ItemDatabase.getOrDiscoverItemFromDescId(int(match.group(1)), self.session)
                item["slot"] = 0
                accessories.append(item)
        else:
            acc1Text = acc1Pattern.search(self.responseText)
            if acc1Text:
                item = ItemDatabase.getOrDiscoverItemFromDescId(int(acc1Text.group(1)), self.session)
                item["slot"] = 1
                accessories.append(item)
            acc2Text = acc2Pattern.search(self.responseText)
            if acc2Text:
                item = ItemDatabase.getOrDiscoverItemFromDescId(int(acc2Text.group(1)), self.session)
                item["slot"] = 2
                accessories.append(item)
            acc3Text = acc3Pattern.search(self.responseText)
            if acc3Text:
                item = ItemDatabase.getOrDiscoverItemFromDescId(int(acc3Text.group(1)), self.session)
                item["slot"] = 3
                accessories.append(item)
        if len(accessories) > 0:
            self.responseData["acc"] = accessories

        famText = familiarPattern.search(self.responseText)
        if famText:
            self.responseData["familiar"] = ItemDatabase.getOrDiscoverItemFromDescId(int(famText.group(1)), self.session)
