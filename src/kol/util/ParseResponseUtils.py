from kol.database import ItemDatabase
from kol.manager import PatternManager

def parseItemsReceived(text, session):
    items = []

    singleItemPattern = PatternManager.getOrCompilePattern('acquireSingleItem')
    for match in singleItemPattern.finditer(text):
        descId = int(match.group(1))
        item = ItemDatabase.getOrDiscoverItemFromDescId(descId, session)
        item["quantity"] = 1
        items.append(item)

    multiItemPattern = PatternManager.getOrCompilePattern('acquireMultipleItems')
    for match in multiItemPattern.finditer(text):
        descId = int(match.group(1))
        quantity = int(match.group(2).replace(',', ''))
        item = ItemDatabase.getOrDiscoverItemFromDescId(descId, session)
        item["quantity"] = quantity
        items.append(item)

    return items

def parseMeatGainedLost(text):
    meatPattern = PatternManager.getOrCompilePattern('gainMeat')
    match = meatPattern.search(text)
    if match:
        return int(match.group(1).replace(',', ''))
    meatPattern = PatternManager.getOrCompilePattern('loseMeat')
    match = meatPattern.search(text)
    if match:
        return -1 * int(match.group(1).replace(',', ''))
    return 0

def parseSubstatsGainedLost(text, checkMuscle=True, checkMysticality=True, checkMoxie=True):
    substats = {}

    if checkMuscle:
        muscPattern = PatternManager.getOrCompilePattern('muscleGainLoss')
        muscMatch = muscPattern.search(text)
        if muscMatch:
            muscle = int(muscMatch.group(2).replace(',', ''))
            if muscMatch.group(1) == "gain":
                substats["muscle"] = muscle
            else:
                substats["muscle"] = -1 * muscle

    if checkMysticality:
        mystPattern = PatternManager.getOrCompilePattern('mysticalityGainLoss')
        mystMatch = mystPattern.search(text)
        if mystMatch:
            myst = int(mystMatch.group(2).replace(',', ''))
            if mystMatch.group(1) == "gain":
                substats["mysticality"] = myst
            else:
                substats["mysticality"] = -1 * myst

    if checkMoxie:
        moxPattern = PatternManager.getOrCompilePattern('moxieGainLoss')
        moxMatch = moxPattern.search(text)
        if moxMatch:
            moxie = int(moxMatch.group(2).replace(',', ''))
            if moxMatch.group(1) == "gain":
                substats["moxie"] = moxie
            else:
                substats["moxie"] = -1 * moxie

    return substats

def parseStatsGainedLost(text, checkMuscle=True, checkMysticality=True, checkMoxie=True):
    """
    Returns a dictionary describing how many stat points the user gained or lost. Please note that
    the user interface does not say how many points were gained or lost if the number is greater
    than 1. This method will return '2' or '-2' in these situations. If your program needs a more
    exact number then you should request the user's character pane.
    """
    statPoints = {}

    if checkMuscle:
        muscPattern = PatternManager.getOrCompilePattern('musclePointGainLoss')
        muscMatch = muscPattern.search(text)
        if muscMatch:
            modifier = 1
            if muscMatch.group(1) == "lose":
                modifier = -1
            if muscMatch.group(2) == 'a':
                statPoints["muscle"] = 1 * modifier
            else:
                statPoints["muscle"] = 2 * modifier

    if checkMysticality:
        mystPattern = PatternManager.getOrCompilePattern('mystPointGainLoss')
        mystMatch = mystPattern.search(text)
        if mystMatch:
            modifier = 1
            if mystMatch.group(1) == "lose":
                modifier = -1
            if mystMatch.group(2) == 'a':
                statPoints["mysticality"] = 1 * modifier
            else:
                statPoints["mysticality"] = 2 * modifier

    if checkMoxie:
        moxPattern = PatternManager.getOrCompilePattern('moxiePointGainLoss')
        moxMatch = moxPattern.search(text)
        if moxMatch:
            modifier = 1
            if moxMatch.group(1) == "lose":
                modifier = -1
            if moxMatch.group(2) == 'a':
                statPoints["moxie"] = 1 * modifier
            else:
                statPoints["moxie"] = 2 * modifier

    return statPoints

def parseLevelsGained(text):
    """
    Returns the number of levels gained by the user during the request. Please note that the user
    interface does not say how many levels were gained if the user gained more than 1. This method
    will return 2 if more than 1 level was gained. If your application needs a more fine-grained
    response, you should check the user's character pane.
    """
    levelPattern = PatternManager.getOrCompilePattern('levelGain')
    levelMatch = levelPattern.search(text)
    if levelMatch:
        if levelMatch.group(1) == "a":
            return 1
        else:
            return 2
    return 0

def parseHPGainedLost(text):
    hp = 0

    # Need to do an iteration because it may happen multiple times in combat.
    hpPattern = PatternManager.getOrCompilePattern('hpGainLoss')
    for hpMatch in hpPattern.finditer(text):
        hpChange = int(hpMatch.group(2).replace(',', ''))
        if hpMatch.group(1) == "gain":
            hp += hpChange
        else:
            hp -= hpChange
    return hp

def parseMPGainedLost(text):
    mp = 0

    # Need to do an iteration because it may happen multiple times in combat
    mpPattern = PatternManager.getOrCompilePattern('mpGainLoss')
    for mpMatch in mpPattern.finditer(text):
        mpChange = int(mpMatch.group(2).replace(',', ''))
        if mpMatch.group(1) == "gain":
            mp += mpChange
        else:
            mp -= mpChange
    return mp

def parseDrunkGained(text):
    drunk = 0
    drunkPattern = PatternManager.getOrCompilePattern('gainDrunk')
    match = drunkPattern.search(text)
    if match:
        drunk = int(match.group(1).replace(',',''))
    return drunk

def parseAdventuresGained(text):
    adventures = 0
    adventurePattern = PatternManager.getOrCompilePattern('gainAdventures')
    match = adventurePattern.search(text)
    if match:
        adventures = int(match.group(1).replace(',',''))
    return adventures

def parseEffectsGained(text):
    effects = []
    effectPattern = PatternManager.getOrCompilePattern('gainEffect')
    for match in effectPattern.finditer(text):
        eff = {}
        eff["name"] = match.group(1)
        eff["turns"] = int(match.group(2).replace(',',''))
        effects.append(eff)
    return effects
