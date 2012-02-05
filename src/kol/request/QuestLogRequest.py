import kol.Error as Error
from GenericRequest import GenericRequest
from kol.manager import PatternManager

class QuestLogRequest(GenericRequest):
    """
    Get info from the quest log about which quests are completed and which stage of each uncompleted quest the player is on
    """

    def __init__(self, session, page):
        super(QuestLogRequest, self).__init__(session)

        # current quests
        #self.url = session.serverURL + "questlog.php?which=1"

        # completed quests
        self.url = session.serverURL + "questlog.php?which=" + str(page)

    def parseResponse(self):

        self.responseData["text"] = self.responseText

        questTitlePattern = PatternManager.getOrCompilePattern("questsCompleted")

        # make a map from quest names to quest descriptions
        quests = {}
        for match in questTitlePattern.finditer(self.responseText):
           quests[match.group(1)] = match.group(2)
        
        """quests = []
        for match in questTitlePattern.finditer(self.responseText):
           quest = {}
           quest["name"] = match.group(1)
           quest["description"] = match.group(2)
           quests.append(quest)"""
        
        self.responseData["quests"] = quests
"""
        noItemPattern = PatternManager.getOrCompilePattern("notEnoughItems")
        match = noItemPattern.search(self.responseText)
        if match:
            raise Error.Error("That item is not in your inventory.", Error.ITEM_NOT_FOUND)

        notEquipmentPattern = PatternManager.getOrCompilePattern("notEquip")
        match = notEquipmentPattern.search(self.responseText)
        if match:
            raise Error.Error("That is not an equippable item.", Error.WRONG_KIND_OF_ITEM)
"""
