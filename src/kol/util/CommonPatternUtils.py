from kol.database import ItemDatabase
from kol.manager import PatternManager
 
import re

"""
Parses whatever text is passed for the requested changes
"""

ALL = 0
MUSCLE = 1
MOXIE = 2
MYST = 3
LEVEL = 4
HP = 5
MP = 6
DRUNK = 7
MEAT = 8
ITEM = 9
ADVEN = 10
EFFECT = 11
HEALTH = 98
STATS = 99

def checkText(text, check=[ALL]):
	if STATS in check:
		check.remove(STATS)
		check.extend([MUSCLE, MOXIE, MYST])
	if HEALTH in check:
		check.remove(HEALTH)
		check.extend([HP, MP])
	
	parsedData={}
	
	statChanges = {}
	
	# Check for level increase if any single stat increase is requested
	if len(set(check).intersection(set([ALL, MUSCLE, MOXIE, MYST, LEVEL]))) > 0:
		if checkLevel(text):
			statChanges["levelGain"] = True	
	
	if ALL in check or MUSCLE in check:
		statChanges.update(checkMuscle(text))
	if ALL in check or MYST in check:
		statChanges.update(checkMyst(text))
	if ALL in check or MOXIE in check:
		statChanges.update(checkMoxie(text))
	
	if ALL in check or HP in check:
		hp = checkHP(text)
		if hp != 0:
			statChanges["hp"] = hp		
	if ALL in check or MP in check:
		mp = checkMP(text)
		if mp != 0:
			statChanges["mp"] = mp
		
	if ALL in check or DRUNK in check:
		drunk = checkDrunk(text)
		if drunk != 0:
			statChanges["drunkGain"] = drunk
			
	if len(statChanges) > 0:
		parsedData["statChange"] = statChanges
		
	if ALL in check or MEAT in check:
		meat = checkMeat(text)
		if meat != 0:
			parsedData["meat"] = meat
		
	if ALL in check or ITEM in check:
		items = checkItem(text)		
		if len(items) > 0:
			parsedData["items"] = items
	
	if ALL in check or ADVEN in check:
		adv = checkAdven(text)
		if adv > 0:
			parsedData["advGain"] = adv
			
	if ALL in check or EFFECT in check:
		effect = checkEffect(text)
		if len(effect) > 0:
			parsedData["effect"] = effect
		
	return parsedData







def checkLevel(text):
	## Check for Level gains
	levelGainPattern = PatternManager.getOrCompilePattern('levelGain')
	
	level = False
	
	match = levelGainPattern.search(text)
	if match:
		level = True
	
	return level


def checkMuscle(text):
	## Check for Muscle changes
	subMuscleGainPattern = PatternManager.getOrCompilePattern('muscleSubstatGain')
	subMuscleLossPattern = PatternManager.getOrCompilePattern('muscleSubstatLoss')
	muscleGainPattern = PatternManager.getOrCompilePattern('musclePointGain')
	muscleLossPattern = PatternManager.getOrCompilePattern('musclePointLoss')
	
	muscleChange = {}
	substat=0
	
	match = subMuscleGainPattern.search(text)
	if match:
		substat = substat + int(match.group(1).replace(',',''))
	match = subMuscleLossPattern.search(text)
	if match:
		substat = substat - int(match.group(1).replace(',',''))
	if substat != 0:
		muscleChange["muscleSub"] = substat
	
	match = muscleGainPattern.search(text)
	if match:
		muscleChange["musclePoint"] = '+'
	match = muscleLossPattern.search(text)
	if match:
		muscleChange["musclePoint"] = '-'
	
	return muscleChange
		
		
def checkMyst(text):
	## Check for Mysticality changes
	subMystGainPattern = PatternManager.getOrCompilePattern('mystSubstatGain')
	subMystLossPattern = PatternManager.getOrCompilePattern('mystSubstatLoss')
	mystGainPattern = PatternManager.getOrCompilePattern('mystPointGain')
	mystLossPattern = PatternManager.getOrCompilePattern('mystPointLoss')
	
	mystChange = {}
	substat=0
	
	match = subMystGainPattern.search(text)
	if match:
		substat = substat + int(match.group(1).replace(',',''))
	match = subMystLossPattern.search(text)
	if match:
		substat = substat - int(match.group(1).replace(',',''))
	if substat != 0:
		mystChange["mystSub"] = substat
	
	match = mystGainPattern.search(text)
	if match:
		mystChange["mystPoint"] = '+'
	match = mystLossPattern.search(text)
	if match:
		mystChange["mystPoint"] = '-'
	
	return mystChange


def checkMoxie(text):
	## Check for Moxie changes
	subMoxieGainPattern = PatternManager.getOrCompilePattern('moxieSubstatGain')
	subMoxieLossPattern = PatternManager.getOrCompilePattern('moxieSubstatLoss')
	moxieGainPattern = PatternManager.getOrCompilePattern('moxiePointGain')
	moxieLossPattern = PatternManager.getOrCompilePattern('moxiePointLoss')
	
	moxieChange = {}
	substat=0
	
	match = subMoxieGainPattern.search(text)
	if match:
		substat = substat + int(match.group(1).replace(',',''))
	match = subMoxieLossPattern.search(text)
	if match:
		substat = substat - int(match.group(1).replace(',',''))
	if substat != 0:
		moxieChange["moxieSub"] = substat
	
	match = moxieGainPattern.search(text)
	if match:
		moxieChange["moxiePoint"] = '+'
	match = moxieLossPattern.search(text)
	if match:
		moxieChange["moxiePoint"] = '-'
	
	return moxieChange


def checkHP(text):
	## Check for HP changes.  We need to iterate for battle situations
	# Where an item AND a familiar/enemy might both affect HP
	hpGainPattern = PatternManager.getOrCompilePattern('hpGain')
	hpLossPattern = PatternManager.getOrCompilePattern('hpLoss')
	
	hp = 0
	
	for match in hpGainPattern.finditer(text):
		hp = hp + int(match.group(1).replace(',',''))
	for match in hpLossPattern.finditer(text):
		hp = hp - int(match.group(1).replace(',',''))
	
	return hp


def checkMP(text):
	## Check for MP changes.  We need to iterate for battle situations
	# Where an item AND a familiar/enemy might both affect MP
	mpGainPattern = PatternManager.getOrCompilePattern('mpGain')
	mpLossPattern = PatternManager.getOrCompilePattern('mpLoss')
	
	mp = 0
	
	for match in mpGainPattern.finditer(text):
		mp = mp + int(match.group(1).replace(',',''))
	for match in mpLossPattern.finditer(text):
		mp = mp - int(match.group(1).replace(',',''))
	
	return mp
	
	
def checkDrunk(text):
	## Check for Drunkenness Changes
	drunkPattern = PatternManager.getOrCompilePattern('gainDrunk')
	
	drunk = 0
	
	match = drunkPattern.search(text)
	if match:
		drunk = int(match.group(1).replace(',',''))
	
	return drunk
		

def checkMeat(text):
	# We won't worry about store transactions here
	gainMeatPattern = PatternManager.getOrCompilePattern("gainMeat")
	loseMeatPattern = PatternManager.getOrCompilePattern("loseMeat")
	
	meat = 0
	
	for match in gainMeatPattern.finditer(text):
		meat = meat + int(match.group(1).replace(',',''))
	for match in loseMeatPattern.finditer(text):
		meat = meat - int(match.group(1).replace(',',''))
	
	return meat


def checkItem(text):
	# Parse for acquired items
	singleItemPattern = PatternManager.getOrCompilePattern('acquireSingleItem')
	multiItemPattern = PatternManager.getOrCompilePattern('acquireMultipleItems')
	
	items = []
	
	for match in singleItemPattern.finditer(text):
		descId = int(match.group(1))
		item = ItemDatabase.getItemFromDescId(descId, self.session)
		item["quantity"] = 1
		items.append(item)
	for match in multiItemPattern.finditer(text):
		descId = int(match.group(1))
		quantity = int(match.group(2).replace(',', ''))
		item = ItemDatabase.getItemFromDescId(descId, self.session)
		item["quantity"] = quantity
		items.append(item)
	
	return items


def checkAdven(text):
	# Parse for adventures gained
	adventurePattern = PatternManager.getOrCompilePattern('gainAdventures')
	
	adventures = 0
	
	match = adventurePattern.search(text)
	if match:
		adventures = int(match.group(1).replace(',',''))
	
	return adventures


def checkEffect(text):
	# Parse for effects acquired
	effectPattern = PatternManager.getOrCompilePattern('gainEffect')
	
	effects = []
	
	for match in effectPattern.finditer(text):
		eff = {}
		eff["name"] = match.group(1)
		eff["turns"] = int(match.group(2).replace(',',''))
		effects.append(eff)
	
	return effects

