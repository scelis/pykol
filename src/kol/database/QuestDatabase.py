"This module is used as a database for KoL quest information."

import kol.Error as Error
from kol.data import Quests
from kol.manager import FilterManager
from kol.util import Report

__isInitialized = False
__questsByName = {}
__councilQuestsByLevel = {}

def init():
    """
    Initializes the QkillDatabase. This method should be called before the
    database is ever accessed as it ensures that the database is populated
    with all of the data it needs.
    """
    global __isInitialized
    if __isInitialized == True:
        return

    Report.trace("questdatabase", "Initializing the quest database.")
    returnCode = FilterManager.executeFiltersForEvent("preInitializeQuestDatabase")
    if returnCode == FilterManager.FINISHED:
        Report.trace("questdatabase", "Quest database initialized.")
        __isInitialized = True
        return

    for quest in Quests.quests:
        addQuest(quest)

    FilterManager.executeFiltersForEvent("postInitializeQuestDatabase")
    __isInitialized = True
    Report.trace("questdatabase", "Quest database initialized.")

"Adds a quest to the database."
def addQuest(quest):
    __questsByName[quest["name"]] = quest
    if quest["source"] == "Council":
        __councilQuestsByLevel[quest["levelAvailable"]] = quest

"Returns information about a quest given its name."
def getQuestFromName(questName, session=None):
    if not __isInitialized:
        init()

    try:
        return __questsByName[questName].copy()
    except KeyError:
        cxt = {}
        FilterManager.executeFiltersForEvent("couldNotFindQuest", cxt, session=session, questName=questName)
        if "quest" in cxt:
            quest = cxt["quest"]
            addQuest(quest)
            return quest.copy()
        raise Error.Error("The quest '%s' is unknown." % questName, Error.QUEST_NOT_FOUND)

def getCouncilQuestFromLevel(questLevel, session=None):
    "Returns information about a quest given its name."
    if not __isInitialized:
        init()

    #print "quest map: " + str(__councilQuestsByLevel)

    try:
        return __councilQuestsByLevel[questLevel].copy()
    except KeyError:
        cxt = {}
        FilterManager.executeFiltersForEvent("couldNotFindQuest", cxt, session=session, questLevel=questLevel)
        if "quest" in cxt:
            quest = cxt["quest"]
            addQuest(quest)
            return quest.copy()
        raise Error.Error("The guild quest for level '%s' is unknown." % questLevel, Error.QUEST_NOT_FOUND)

