import kol.Error as Error
from kol.database import ItemDatabase
from kol.serialize import ItemsSerializer

import re
import urllib2

CONCOCTIONS_FILE = "https://kolmafia.svn.sourceforge.net/svnroot/kolmafia/src/data/concoctions.txt"
EQUIPMENT_FILE = "https://kolmafia.svn.sourceforge.net/svnroot/kolmafia/src/data/equipment.txt"
FOLD_GROUPS_FILE = "https://kolmafia.svn.sourceforge.net/svnroot/kolmafia/src/data/foldgroups.txt"
FULLNESS_FILE = "https://kolmafia.svn.sourceforge.net/svnroot/kolmafia/src/data/fullness.txt"
INEBRIETY_FILE = "https://kolmafia.svn.sourceforge.net/svnroot/kolmafia/src/data/inebriety.txt"
ITEM_DESCS_FILE = "https://kolmafia.svn.sourceforge.net/svnroot/kolmafia/src/data/items.txt"
MODIFIERS_FILE = "https://kolmafia.svn.sourceforge.net/svnroot/kolmafia/src/data/modifiers.txt"
NPC_STORES_FILE = "https://kolmafia.svn.sourceforge.net/svnroot/kolmafia/src/data/npcstores.txt"
OUTFITS_FILE = "https://kolmafia.svn.sourceforge.net/svnroot/kolmafia/src/data/outfits.txt"
PACKAGES_FILE = "https://kolmafia.svn.sourceforge.net/svnroot/kolmafia/src/data/packages.txt"
SPLEEN_FILE = "https://kolmafia.svn.sourceforge.net/svnroot/kolmafia/src/data/spleenhit.txt"
ZAP_GROUPS_FILE = "https://kolmafia.svn.sourceforge.net/svnroot/kolmafia/src/data/zapgroups.txt"

REQUIRED_MUSCLE_PATTERN = re.compile("Mus: ([0-9]+)")
REQUIRED_MYSTICALITY_PATTERN = re.compile("Mys: ([0-9]+)")
REQUIRED_MOXIE_PATTERN = re.compile("Mox: ([0-9]+)")
INTRINSIC_PATTERN = re.compile('Intrinsic Effect: "([^"]+)"')
CLASS_PATTERN = re.compile('Class: "([^"]+)"')

ENCHANTMENT_MAPPINGS = {
    'Adventures' : 'adventuresAtRollover',
    'Cold Damage' : 'coldDamage',
    'Cold Resistance' : 'coldResistance',
    'Cold Spell Damage' : 'coldSpellDamage',
    'Critical' : 'critical',
    'Damage Absorption' : 'damageAbsorption',
    'Fumble' : 'fumble',
    'Hobo Power' : 'hoboPower',
    'Hot Damage' : 'hotDamage',
    'Hot Resistance' : 'hotResistance',
    'Hot Spell Damage' : 'hotSpellDamage',
    'Initiative' : 'initiative',
    'Item Drop' : 'itemDrop',
    'Maximum HP' : 'maximumHP',
    'Maximum MP' : 'maximumMP',
    'Meat Drop' : 'meatDrop',
    'Melee Damage' : 'weaponDamage',
    'Moxie Percent' : 'moxiePercent',
    'Muscle Percent' : 'musclePercent',
    'Mysticality Percent' : 'mysticalityPercent',
    'Moxie' : 'moxie',
    'Muscle' : 'muscle',
    'Mysticality' : 'mysticality',
    'Ranged Damage' : 'rangedDamage',
    'Sleaze Damage' : 'sleazeDamage',
    'Sleaze Resistance' : 'sleazeResistance',
    'Sleaze Spell Damage' : 'sleazeSpellDamage',
    'Spell Damage' : 'spellDamage',
    'Spell Damage Percent' : 'spellDamagePercent',
    'Spooky Damage' : 'spookyDamage',
    'Spooky Resistance' : 'spookyResistance',
    'Spooky Spell Damage' : 'spookySpellDamage',
    'Stench Damage' : 'stenchDamage',
    'Stench Resistance' : 'stenchResistance',
    'Stench Spell Damage' : 'stenchSpellDamage',
    'Weapon Damage' : 'weaponDamage'
}

GIFT_PACKAGES = [
    "raffle prize box",
    "Warehouse 23 crate",
    "anniversary gift box",
    "bindle of joy",
    "moist sack",
    "foreign box",
    "Uncle Crimbo's Sack"
]

_items = []
_itemsById = {}
_itemsByName = {}
_opener = urllib2.build_opener()


def main():
    readItemDescsFile()
    readEquipmentFile()
    readFullnessFile()
    readInebrietyFile()
    readSpleenFile()
    readPackagesFile()
    readOutfitsFile()
    readZapGroupsFile()
    readFoldGroupsFile()
    readNPCStoresFile()
    readModifiersFile()
    fixupItems()
    writeItems()


def itemByName(name):
    return _itemsByName[name.lower()]


def readItemDescsFile():
    text = _opener.open(ITEM_DESCS_FILE).read()
    for line in text.splitlines():
        if len(line) > 0 and line[0] != '#':
            parts = line.split('\t')
            if len(parts) >= 3:
                itemId = int(parts[0])
                name = parts[1]
                descId = int(parts[2])
                image = parts[3]
                item = {"id" : itemId, "descId" : descId, "name" : name, "image" : image}

                itemTypes = parts[4].split(',')
                for i in range(len(itemTypes)):
                    itemTypes[i] = itemTypes[i].strip()
                itemTradeStr = parts[5]
                autosell = 0
                if len(parts[6]) > 0:
                    autosell = int(parts[6])

                if autosell > 0:
                    item["autosell"] = autosell

                if "food" in itemTypes:
                    item["type"] = "food"
                elif "drink" in itemTypes:
                    item["type"] = "booze"
                elif "grow" in itemTypes:
                    item["type"] = "familiar"
                elif "familiar" in itemTypes:
                    item["type"] = "familiar equipment"

                if "mp" in itemTypes or "hp" in itemTypes or "hpmp" in itemTypes or "usable" in itemTypes or "message" in itemTypes:
                    item["isUsable"] = True
                if "multiple" in itemTypes:
                    item["isUsable"] = True
                    item["isMultiUsable"] = True
                if "reusable" in itemTypes:
                    item["isUsable"] = True
                    item["isReusable"] = True
                if "zap" in itemTypes:
                    item["isZappable"] = True
                if "sphere" in itemTypes:
                    item["isSphere"] = True
                if "combat" in itemTypes:
                    item["isCombatUsable"] = True
                if "combat reusable" in itemTypes:
                    item["isCombatUsable"] = True
                    item["isCombatReusable"]  = True
                if "curse" in itemTypes:
                    item["isUsableOnOthers"] = True
                if "bounty" in itemTypes:
                    item["isBounty"] = True
                if "candy" in itemTypes:
                    item["isCandy"] = True

                if "type" not in item:
                    if "isUsable" in item and item["isUsable"] and "isCombatUsable" in item and item["isCombatUsable"]:
                        item["type"] = "combat / usable item"
                    elif "isUsable" in item and item["isUsable"]:
                        item["type"] = "usable"
                    elif "isCombatUsable" in item and item["isCombatUsable"]:
                        item["type"] = "combat item"

                if len(parts) > 7:
                    plural = parts[7]
                    if plural != name + 's':
                        item["plural"] = plural

                _items.append(item)
                _itemsById[itemId] = item
                _itemsByName[name.lower()] = item


def readEquipmentFile():
    currentType = None
    text = _opener.open(EQUIPMENT_FILE).read()
    for line in text.splitlines():
        if len(line) > 0:
            if line[0] == '#':
                if line.find('Hats section') >= 0:
                    currentType = "hat"
                elif line.find('Pants section') >= 0:
                    currentType = "pants"
                elif line.find('Shirts section') >= 0:
                    currentType = "shirt"
                elif line.find('Weapons section') >= 0:
                    currentType = "weapon"
                elif line.find('Off-hand section') >= 0:
                    currentType = "off-hand"
                elif line.find('Accessories section') >= 0:
                    currentType = "accessory"
                elif line.find('Containers section') >= 0:
                    currentType = "container"
            else:
                parts = line.split('\t')
                if len(parts) >= 3:
                    name = parts[0]
                    power = int(parts[1])
                    requirements = parts[2]
                    if currentType == "weapon":
                        weaponType = parts[3]
                    elif currentType == "off-hand":
                        if len(parts) >= 4:
                            offHandType = parts[3]
                        else:
                            offHandType = ""

                    try:
                        item = itemByName(name)
                    except KeyError:
                        continue

                    # Set the power
                    if power > 0 or currentType == "weapon" or (currentType == "off-hand" and offHandType == "shield"):
                        item["power"] = power

                    # Set the requirements
                    if len(requirements) > 0 and requirements != "none":
                        muscleMatch = REQUIRED_MUSCLE_PATTERN.search(requirements)
                        if muscleMatch:
                            muscle = int(muscleMatch.group(1))
                            item["requiredMuscle"] = muscle
                        mysticalityMatch = REQUIRED_MYSTICALITY_PATTERN.search(requirements)
                        if mysticalityMatch:
                            myst = int(mysticalityMatch.group(1))
                            item["requiredMysticality"] = myst
                        moxieMatch = REQUIRED_MOXIE_PATTERN.search(requirements)
                        if moxieMatch:
                            moxie = int(moxieMatch.group(1))
                            item["requiredMoxie"] = moxie

                    # Set the type
                    if currentType == "weapon":
                        item["type"] = "weapon (%s)" % weaponType
                    elif currentType == "off-hand":
                        if len(offHandType) > 0:
                            item["type"] = "off-hand item (%s)" % offHandType
                        else:
                            item["type"] = "off-hand item"
                    else:
                        item["type"] = currentType


def readFullnessFile():
    text = _opener.open(FULLNESS_FILE).read()
    for line in text.splitlines():
        if len(line) > 0 and line[0] != '#':
            parts = line.split('\t')
            if len(parts) >= 8:
                name = parts[0]
                fullness = int(parts[1])
                level = int(parts[2])
                quality = parts[3]
                adv = parts[4]
                musc = parts[5]
                myst = parts[6]
                mox = parts[7]

                try:
                    item = itemByName(name)
                except KeyError:
                    continue

                if fullness > 0:
                    item["fullness"] = fullness
                if level > 0:
                    item["levelRequired"] = level
                if len(quality) > 0:
                    item["quality"] = quality
                if adv != "0" and len(adv) > 0:
                    item["adventuresGained"] = adv
                if musc != "0" and len(musc) > 0:
                    item["muscleGained"] = musc
                if myst != "0" and len(myst) > 0:
                    item["mysticalityGained"] = myst
                if mox != "0" and len(mox) > 0:
                    item["moxieGained"] = mox


def readInebrietyFile():
    text = _opener.open(INEBRIETY_FILE).read()
    for line in text.splitlines():
        if len(line) > 0 and line[0] != '#':
            parts = line.split('\t')
            if len(parts) >= 8:
                name = parts[0]
                drunkenness = int(parts[1])
                level = int(parts[2])
                quality = parts[3]
                adv = parts[4]
                musc = parts[5]
                myst = parts[6]
                mox = parts[7]
                if name == "ice-cold Sir Schlitz":
                    print quality
                    print drunkenness

                try:
                    item = itemByName(name)
                except KeyError:
                    continue

                if drunkenness > 0:
                    item["drunkenness"] = drunkenness
                if level > 0:
                    item["levelRequired"] = level
                if len(quality) > 0:
                    item["quality"] = quality
                if adv != "0" and len(adv) > 0:
                    item["adventuresGained"] = adv
                if musc != "0" and len(musc) > 0:
                    item["muscleGained"] = musc
                if myst != "0" and len(myst) > 0:
                    item["mysticalityGained"] = myst
                if mox != "0" and len(mox) > 0:
                    item["moxieGained"] = mox


def readSpleenFile():
    text = _opener.open(SPLEEN_FILE).read()
    for line in text.splitlines():
        if len(line) > 0 and line[0] != '#':
            parts = line.split('\t')
            if len(parts) >= 8:
                name = parts[0]
                spleen = int(parts[1])
                level = int(parts[2])
                quality = parts[3]
                adv = parts[4]
                musc = parts[5]
                myst = parts[6]
                mox = parts[7]

                try:
                    item = itemByName(name)
                except KeyError:
                    continue

                if spleen > 0:
                    item["spleen"] = spleen
                if level > 0:
                    item["levelRequired"] = level
                if len(quality) > 0:
                    item["quality"] = quality
                if adv != "0" and len(adv) > 0:
                    item["adventuresGained"] = adv
                if musc != "0" and len(musc) > 0:
                    item["muscleGained"] = musc
                if myst != "0" and len(myst) > 0:
                    item["mysticalityGained"] = myst
                if mox != "0" and len(mox) > 0:
                    item["moxieGained"] = mox


def readPackagesFile():
    text = _opener.open(PACKAGES_FILE).read()
    for line in text.splitlines():
        if len(line) > 0 and line[0] != '#':
            parts = line.split('\t')
            if len(parts) >= 4:
                name = parts[0]
                numItems = int(parts[2])
                price = int(parts[3])

                try:
                    item = itemByName(name)
                except KeyError:
                    continue

                item["type"] = "gift package"
                item["numPackageItems"] = numItems
                item["npcPrice"] = price


def readOutfitsFile():
    text = _opener.open(OUTFITS_FILE).read()
    for line in text.splitlines():
        if len(line) > 0 and line[0] != '#':
            parts = line.split('\t')
            if len(parts) >= 3:
                outfitId = int(parts[0])
                outfitName = parts[1]
                outfitItems = parts[2].split(',')
                for thisItem in outfitItems:
                    thisItem = thisItem.strip()
                    try:
                        item = itemByName(thisItem)
                    except KeyError:
                        continue
                    item["outfit"] = outfitName
                    item["outfitId"] = outfitId


def readZapGroupsFile():
    text = _opener.open(ZAP_GROUPS_FILE).read()
    for line in text.splitlines():
        if len(line) > 1 and line[0] != '#':
            zapItems = line.split(',')
            for thisItem in zapItems:
                thisItem = thisItem.strip()
                try:
                    item = itemByName(thisItem)
                except KeyError:
                    continue
                item["isZappable"] = True


def readFoldGroupsFile():
    text = _opener.open(FOLD_GROUPS_FILE).read()
    for line in text.splitlines():
        if len(line) > 1 and line[0] != '#':
            foldItems = line.split(',')
            for thisItem in foldItems:
                thisItem = thisItem.strip()
                try:
                    item = itemByName(thisItem)
                except KeyError:
                    continue
                item["isFoldable"] = True


def readNPCStoresFile():
    text = _opener.open(NPC_STORES_FILE).read()
    for line in text.splitlines():
        if len(line) > 0 and line[0] != '#':
            parts = line.split('\t')
            if len(parts) >= 3:
                storeName = parts[0]
                storeId = parts[1]
                itemName = parts[2]
                price = int(parts[3])
                try:
                    item = itemByName(itemName)
                except KeyError:
                    continue
                item["npcStoreId"] = storeId
                item["npcPrice"] = price


def readModifiersFile():
    text = _opener.open(MODIFIERS_FILE).read()
    for line in text.splitlines():
        if line == "# Special case overrides":
            break

        if len(line) > 0 and line[0] != '#':
            parts = line.split('\t')
            if len(parts) >= 2:
                itemName = parts[0]
                modifiers = parts[1].strip()

                try:
                    item = itemByName(itemName)
                    item["enchantments"] = {}
                except KeyError:
                    continue

                classMatch = CLASS_PATTERN.search(modifiers)
                if classMatch:
                    item["classes"] = []
                    classes = classMatch.group(1)
                    classes = classes.split(',')
                    for aClass in classes:
                        item["classes"].append(aClass.strip())
                    modifiers = CLASS_PATTERN.sub('', modifiers)
                    modifiers = modifiers.strip(' ,')

                intrinsicMatch = INTRINSIC_PATTERN.search(modifiers)
                if intrinsicMatch:
                    item["enchantments"] = {}
                    item["enchantments"]["intrinsicEffects"] = []

                    intrinsics = intrinsicMatch.group(1)
                    intrinsics = intrinsics.split(',')
                    for intrinsic in intrinsics:
                        item["enchantments"]["intrinsicEffects"].append(intrinsic.strip())
                    modifiers = INTRINSIC_PATTERN.sub('', modifiers)
                    modifiers = modifiers.strip(' ,')

                if len(modifiers) == 0:
                    continue

                modifiers = modifiers.split(',')
                for modifier in modifiers:
                    modifier = modifier.strip()
                    if len(modifier) == 0:
                        continue
                    elif modifier == "Single Equip":
                        item["isMaxEquipOne"] = True
                    elif modifier == "Softcore Only":
                        item["isSoftcoreOnly"] = True
                    elif modifier == "Hobo Powered":
                        item["isHoboPowered"] = True
                    else:
                        if "enchantments" not in item:
                            item["enchantments"] = {}

                        if modifier == "Never Fumble":
                            item["enchantments"]["neverFumble"] = True
                        elif modifier == "Weakens Monster":
                            item["enchantments"]["weakensMonster"] = True
                        else:
                            modifier = modifier.split(':')
                            if len(modifier) >= 2:
                                item["enchantments"][modifier[0].strip()] = modifier[1].strip()

                if "enchantments" in item and len(item["enchantments"]) == 0:
                    del item["enchantments"]


def fixupItems():
    for item in _items:
        if "enchantments" in item:
            if len(item["enchantments"]) == 0:
                del item["enchantments"]
            else:
                enchantments = item["enchantments"]
                if "MP Regen Min" in enchantments:
                    min = enchantments["MP Regen Min"]
                    max = enchantments["MP Regen Max"]
                    del enchantments["MP Regen Min"]
                    del enchantments["MP Regen Max"]
                    enchantments["mpRegen"] = "%s-%s" % (min, max)
                if "HP Regen Min" in enchantments:
                    min = enchantments["HP Regen Min"]
                    max = enchantments["HP Regen Max"]
                    del enchantments["HP Regen Min"]
                    del enchantments["HP Regen Max"]
                    enchantments["hpRegen"] = "%s-%s" % (min, max)
                for k,v in ENCHANTMENT_MAPPINGS.iteritems():
                    if k in enchantments:
                        enchantments[v] = enchantments[k]
                        del enchantments[k]
    for itemName in GIFT_PACKAGES:
        try:
            item = itemByName(itemName)
            item["type"] = "gift package"
        except KeyError:
            pass


def writeItems():
    f = open("Items.py", "w")
    ItemsSerializer.writeItems(_items, f)

if __name__ == "__main__":
    main()

