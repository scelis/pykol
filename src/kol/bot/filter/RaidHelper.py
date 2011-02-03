"""
This module implements a FilterManager filter to provide extra information
about clan dungeons. It currently listens to chat and parses the Hobopolis
logs to see the current status of the dungeon. It can report how many turns
have been spent in each area, as well as who is currently trapped in the
CHUM cage.
"""

from kol.bot import BotUtils
from kol.manager import FilterManager
from kol.manager import PatternManager
from kol.request.ClanRaidLogRequest import ClanRaidLogRequest
from kol.util import NumberUtils

HOBOPOLIS_AREAS = [
    "Town Square",
    "Burnbarrel Blvd.",
    "Exposure Esplanade",
    "The Heap",
    "The Ancient Hobo Burial Ground",
    "The Purple Light District",
]

HOBOPOLIS_BOSSES = {
    "Town Square" : "Hodgman, The Hoboverlord",
    "Burnbarrel Blvd." : "Ol' Scratch",
    "Exposure Esplanade" : "Frosty",
    "The Heap" : "Oscus",
    "The Ancient Hobo Burial Ground" : "Zombo",
    "The Purple Light District" : "Chester",
}

HOBOPOLIS_AREA_SHORT_NAMES = {
    "Town Square" : "TS",
    "Burnbarrel Blvd." : "BB",
    "Exposure Esplanade" : "EE",
    "The Heap" : "Heap",
    "The Ancient Hobo Burial Ground" : "BG",
    "The Purple Light District" : "PLD",
}

def doFilter(eventName, context, **kwargs):
    returnCode = FilterManager.CONTINUE
    if eventName == "botProcessChat":
        returnCode = botProcessChat(context, **kwargs)
    return returnCode

def botProcessChat(context, **kwargs):
    returnCode = FilterManager.CONTINUE
    chat = kwargs["chat"]
    bot = kwargs["bot"]

    if chat["type"] == "private":
        if chat["text"] == "hobo status":
            reportHobopolisStatus(context, **kwargs)
            returnCode = FilterManager.FINISHED
    elif chat["type"] == "normal" and chat["userId"] == -2:
        parseDungeonChatMessage(context, **kwargs)

    return returnCode

def reportHobopolisStatus(context, **kwargs):
    bot = kwargs["bot"]
    chat = kwargs["chat"]
    state = bot.states["global"]

    r = ClanRaidLogRequest(bot.session)
    data = r.doRequest()

    whitespacePattern = PatternManager.getOrCompilePattern('whitespace')

    numGrates = 0
    numValves = 0
    totalTurns = 0
    areas = {}
    for area in HOBOPOLIS_AREAS:
        areas[area] = {"turns" : 0}
    for event in data["events"]:
        event["event"] = whitespacePattern.sub(' ', event["event"])
        if "turns" in event:
            totalTurns += event["turns"]
        if event["category"] == "Sewers":
            if event["event"].find("lowered the water level") >= 0:
                numValves += event["turns"]
            elif event["event"].find("sewer grate") >= 0:
                numGrates += event["turns"]
        elif event["category"] in HOBOPOLIS_AREAS:
            areaName = event["category"]
            areas[areaName]["turns"] += event["turns"]
            bossName = HOBOPOLIS_BOSSES[areaName]
            if event["event"].find("defeated %s" % bossName) >= 0:
                areas[areaName]["completed"] = True
        elif event["category"] == "Miscellaneous":
            bossName = HOBOPOLIS_BOSSES["Town Square"]
            if event["event"].find("defeated %s" % bossName) >= 0:
                areas["Town Square"]["completed"] = True
                areas["Town Square"]["turns"] += event["turns"]

    resp = "[Sewer: valves=%s/20, grates=%s/20" % (numValves, numGrates)
    if "hobo:sewerTrapped" in state:
        resp += ", trapped=%s" % state["hobo:sewerTrapped"]
    resp += ']'

    for areaName in HOBOPOLIS_AREAS:
        areaData = areas[areaName]
        completed = ("completed" in areaData)
        turns = areaData["turns"]

        if completed:
            resp += " [%s: DONE]" % HOBOPOLIS_AREA_SHORT_NAMES[areaName]
        else:
            if turns == 1:
                resp += " [%s: %s turn" % (HOBOPOLIS_AREA_SHORT_NAMES[areaName], turns)
            else:
                turnsStr = NumberUtils.formatNumberWithCommas(turns)
                resp += " [%s: %s turns" % (HOBOPOLIS_AREA_SHORT_NAMES[areaName], turnsStr)

            if turns > 0:
                if areaName == "Burnbarrel Blvd.":
                    numTires = 0
                    if "hobo:tiresStacked" in state:
                        numTires = state["hobo:tiresStacked"]
                    resp += ", %s tires" % numTires

            resp += ']'

    resp += ' [TOTAL: %s turns]' % totalTurns

    bot.sendChatMessage("/w %s %s" % (chat["userId"], resp))

def parseDungeonChatMessage(context, **kwargs):
    chat = kwargs["chat"]
    bot = kwargs["bot"]
    state = bot.states["global"]

    trappedPattern = PatternManager.getOrCompilePattern('imprisonedByChums')
    rescuedPattern = PatternManager.getOrCompilePattern('freedFromChums')

    if chat["text"].find("has put a tire on the fire") > 0:
        numTires = 0
        if "hobo:tiresStacked" in state:
            numTires = state["hobo:tiresStacked"]
        numTires += 1
        state["hobo:tiresStacked"] = numTires
        bot.writeState("global")
    elif chat["text"].find("has started a tirevalanche") > 0:
        state["hobo:tiresStacked"] = 0
        bot.writeState("global")
    elif chat["text"].find("escaped from the C. H. U. M.s by gnawing through their cage") > 0 or rescuedPattern.match(chat["text"]):
        if "hobo:sewerTrapped" in state:
            del state["hobo:sewerTrapped"]
            bot.writeState("global")
    elif chat["text"].find("flooded the sewers leading to Hobopolis") > 0:
        keysToClear = ["hobo:sewerTrapped", "hobo:tiresStacked"]
        for key in keysToClear:
            if key in state:
                del state[key]
        bot.writeState("global")
    else:
        match = trappedPattern.match(chat["text"])
        if match:
            state["hobo:sewerTrapped"] = match.group(1)
            bot.writeState("global")
