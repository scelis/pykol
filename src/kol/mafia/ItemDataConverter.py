from kol.Error import ItemNotFoundError
from kol.Session import Session
from kol.database import ItemDatabase
from kol.request.ItemDescriptionRequest import ItemDescriptionRequest
from kol.serialize import ItemsSerializer

import re
import sys
import urllib2

EQUIPMENT_FILE = "https://kolmafia.svn.sourceforge.net/svnroot/kolmafia/src/data/equipment.txt"
FULLNESS_FILE = "https://kolmafia.svn.sourceforge.net/svnroot/kolmafia/src/data/fullness.txt"
INEBRIETY_FILE = "https://kolmafia.svn.sourceforge.net/svnroot/kolmafia/src/data/inebriety.txt"
ITEM_DESCS_FILE = "https://kolmafia.svn.sourceforge.net/svnroot/kolmafia/src/data/itemdescs.txt"
MODIFIERS_FILE = "https://kolmafia.svn.sourceforge.net/svnroot/kolmafia/src/data/modifiers.txt"
OUTFITS_FILE = "https://kolmafia.svn.sourceforge.net/svnroot/kolmafia/src/data/outfits.txt"
PACKAGES_FILE = "https://kolmafia.svn.sourceforge.net/svnroot/kolmafia/src/data/packages.txt"
SPLEEN_FILE = "https://kolmafia.svn.sourceforge.net/svnroot/kolmafia/src/data/spleenhit.txt"
TRADE_ITEMS_FILE = "https://kolmafia.svn.sourceforge.net/svnroot/kolmafia/src/data/tradeitems.txt"
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
	'Melee Damage' : 'meleeDamage',
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
}

_items = []
_itemsById = {}
_itemsByName = {}
_opener = urllib2.build_opener()
_session = None

def main(argv=sys.argv):
	login(argv[1], argv[2])
	readItemDescsFile()
	readEquipmentFile()
	readFullnessFile()
	readInebrietyFile()
	readSpleenFile()
	readPackagesFile()
	readOutfitsFile()
	readZapGroupsFile()
	readTradeItemsFile()
	readModifiersFile()
	fixupItems()
	mergeItems()
	_session.logout()
	writeItems()

def login(username, password):
	global _session
	_session = Session()
	_session.login(username, password)

def readItemDescsFile():
	text = _opener.open(ITEM_DESCS_FILE).read()
	for line in text.splitlines():
		if len(line) > 0 and line[0] != '#':
			parts = line.split('\t')
			if len(parts) >= 3:
				itemId = int(parts[0])
				descId = int(parts[1])
				name = parts[2]
				item = {"id" : int(parts[0]), "descId" : int(parts[1]), "name" : parts[2]}
				
				if len(parts) > 3:
					plural = parts[3]
					if plural != name + 's':
						item["plural"] = parts[3]
				
				_items.append(item)
				_itemsById[itemId] = item
				_itemsByName[name] = item

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
						item = _itemsByName[name]
					except KeyError:
						continue
					
					# Set the power
					if power > 0 or currentType == "weapon" or \
						(currentType == "off-hand" and offHandType == "shield"):
						item["power"] = power
					
					# Set the requirements
					if len(requirements) > 0 and requirements != "none":
						muscleMatch = REQUIRED_MUSCLE_PATTERN.search(requirements)
						if muscleMatch:
						 	muscle = int(muscleMatch.group(1))
							if muscle > 0:
								item["requiredMuscle"] = muscle
						mysticalityMatch = REQUIRED_MYSTICALITY_PATTERN.search(requirements)
						if mysticalityMatch:
						 	myst = int(mysticalityMatch.group(1))
							if myst > 0:
								item["requiredMysticality"] = myst
						moxieMatch = REQUIRED_MOXIE_PATTERN.search(requirements)
						if moxieMatch:
						 	moxie = int(moxieMatch.group(1))
							if moxie > 0:
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
			if len(parts) >= 7:
				name = parts[0]
				fullness = int(parts[1])
				level = int(parts[2])
				adv = parts[3]
				musc = parts[4]
				myst = parts[5]
				mox = parts[6]
				
				try:
					item = _itemsByName[name]
				except KeyError:
					continue
				
				if fullness > 0:
					item["fullness"] = fullness
				if level > 0:
					item["levelRequired"] = level
				if adv != "0":
					item["adventuresGained"] = adv
				if musc != "0":
					item["muscleGained"] = musc
				if myst != "0":
					item["mysticalityGained"] = myst
				if mox != "0":
					item["moxieGained"] = mox

def readInebrietyFile():
	text = _opener.open(INEBRIETY_FILE).read()
	for line in text.splitlines():
		if len(line) > 0 and line[0] != '#':
			parts = line.split('\t')
			if len(parts) >= 7:
				name = parts[0]
				drunkenness = int(parts[1])
				level = int(parts[2])
				adv = parts[3]
				musc = parts[4]
				myst = parts[5]
				mox = parts[6]
				
				try:
					item = _itemsByName[name]
				except KeyError:
					continue
				
				if drunkenness > 0:
					item["drunkenness"] = drunkenness
				if level > 0:
					item["levelRequired"] = level
				if adv != "0":
					item["adventuresGained"] = adv
				if musc != "0":
					item["muscleGained"] = musc
				if myst != "0":
					item["mysticalityGained"] = myst
				if mox != "0":
					item["moxieGained"] = mox

def readSpleenFile():
	text = _opener.open(SPLEEN_FILE).read()
	for line in text.splitlines():
		if len(line) > 0 and line[0] != '#':
			parts = line.split('\t')
			if len(parts) >= 7:
				name = parts[0]
				spleen = int(parts[1])
				level = int(parts[2])
				adv = parts[3]
				musc = parts[4]
				myst = parts[5]
				mox = parts[6]
				
				try:
					item = _itemsByName[name]
				except KeyError:
					continue
				
				if spleen > 0:
					item["spleen"] = spleen
				if level > 0:
					item["levelRequired"] = level
				if adv != "0":
					item["adventuresGained"] = adv
				if musc != "0":
					item["muscleGained"] = musc
				if myst != "0":
					item["mysticalityGained"] = myst
				if mox != "0":
					item["moxieGained"] = mox

def readPackagesFile():
	text = _opener.open(PACKAGES_FILE).read()
	for line in text.splitlines():
		if len(line) > 0 and line[0] != '#':
			parts = line.split('\t')
			if len(parts) >= 4:
				name = parts[0]
				numItems = int(parts[1])
				
				try:
					item = _itemsByName[name]
				except KeyError:
					continue
				
				item["numPackageItems"] = numItems

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
						item = _itemsByName[thisItem]
					except KeyError:
						continue
					item["outfit"] = outfitName

def readZapGroupsFile():
	text = _opener.open(ZAP_GROUPS_FILE).read()
	for line in text.splitlines():
		if len(line) > 1 and line[0] != '#':
			zapItems = line.split(',')
			for thisItem in zapItems:
				thisItem = thisItem.strip()
				try:
					item = _itemsByName[thisItem]
				except KeyError:
					continue
				item["isZappable"] = True

def readTradeItemsFile():
	text = _opener.open(TRADE_ITEMS_FILE).read()
	for line in text.splitlines():
		if len(line) > 0 and line[0] != '#':
			parts = line.split('\t')
			if len(parts) >= 5:
				itemId = int(parts[0])
				itemName = parts[1]
				itemTypeId = parts[2]
				itemTradeStr = parts[3]
				autosell = int(parts[4])
				
				try:
					item = _itemsById[itemId]
				except KeyError:
					continue
				
				if autosell > 0:
					item["autosell"] = autosell
				
				if itemTypeId == "usable":
					item["isUsable"] = True
				elif itemTypeId == "multiple":
					item["isUsable"] = True
					item["isMultiUsable"] = True
				elif itemTypeId == "grow":
					item["type"] = "familiar"
				elif itemTypeId == "familiar":
					item["type"] = "familiar equipment"
				elif itemTypeId == "reusable":
					item["isUsable"] = True
					item["notConsumedWhenUsed"] = True

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
					item = _itemsByName[itemName]
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

def mergeItems():
	ItemDatabase.init()
	for i in range(len(_items)):
		item = _items[i]
		try:
			savedItem = ItemDatabase.getItemFromId(item["id"])
			
			for k,v in item.iteritems():
				if k != "enchantments" and k != "type":
					savedItem[k] = v
			if "enchantments" in item and len(item["enchantments"]) > 0:
				if "enchantments" not in savedItem:
					savedItem["enchantments"] = {}
				for k,v in item["enchantments"].iteritems():
					savedItem["enchantments"][k] = v
			_items[i] = savedItem
		except ItemNotFoundError:
			r = ItemDescriptionRequest(_session, item["descId"])
			itemInfo = r.doRequest()
			for k,v in itemInfo.iteritems():
				item[k] = v

def writeItems():
	f = open("Items.py", "w")
	ItemsSerializer.writeItems(_items, f)

if __name__ == "__main__":
    main()

