ITEM_ATTRIBUTES = [
	'id',
	'descId',
	'name',
	'plural',
	'type',
	'outfit',
	'image',
	'autosell',
	'isUsable',
	'isMultiUsable',
	'notConsumedWhenUsed',
	'cannotBeTraded',
	'requiredLevel',
	'requiredMuscle',
	'requiredMysticality',
	'requiredMoxie',
	'isSoftcoreOnly',
	'isMaxEquipOne',
	'fullness',
	'drunkenness',
	'spleen',
	'adventuresGained',
	'muscleGained',
	'mysticalityGained',
	'moxieGained',
	'isCookingIngredient',
	'isCocktailcraftingIngredient',
	'isMeatsmithingComponent',
	'isJewelrymakingComponent',
	'numPackageItems',
	'isZappable',
	'enchantments',
]

ITEM_ENCHANTMENTS = [
	'muscle',
	'mysticality',
	'moxie',
	
	'familiarWeight',
	'itemDrop',
	'meatDrop',
	
	'initiative',
	'critical',
	'fumble',
	'damageAbsorption',
	
	'hpRegen',
	'mpRegen',
	'maximumHP',
	'maximumMP',
	
	'meleeDamage',
	'rangedDamage',
	'coldDamage',
	'hotDamage',
	'sleazeDamage',
	'spookyDamage',
	'stenchDamage',
	'spellDamage',
	
	'coldSpellDamage',
	'hotSpellDamage',
	'sleazeSpellDamage',
	'spookySpellDamage',
	'stenchSpellDamage',
	
	'coldResistance',
	'hotResistance',
	'sleazeResistance',
	'spookyResistance',
	'stenchResistance',
]

def writeItems(out, items):
	out.write("# $I" + "d$\n\n")
	out.write("items = [\n")
	
	for item in items:
		out.write("\t{\n")
		for attribute in ITEM_ATTRIBUTES:
			if attribute in item:
				val = item[attribute]
				if type(val) == int or type(val) == bool:
					out.write('\t\t"%s" : %s,\n' % (attribute, val))
				elif type(val) == str:
					out.write('\t\t"%s" : "%s",\n' % (attribute, val))
				elif type(val) == list:
					out.write('\t\t"%s" : %s,\n' % (attribute, str(val)))
				elif attribute == "enchantments":
					out.write('\t\t"%s" :\n' % attribute)
					out.write('\t\t{\n')
					for enchantment in ITEM_ENCHANTMENTS:
						if enchantment in val:
							enVal = val[enchantment]
							if type(enVal) == int or type(enVal) == bool:
								out.write('\t\t\t"%s" : %s,\n' % (enchantment, enVal))
							elif type(enVal) == str:
								out.write('\t\t\t"%s" : "%s",\n' % (enchantment, enVal))
							elif type(enVal) == list:
								out.write('\t\t\t"%s" : %s,\n' % (enchantment, str(enVal)))
					out.write('\t\t},\n')
		out.write("\t},\n")
	out.write(']\n')
