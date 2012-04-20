ITEM_ATTRIBUTES = [
    'id',
    'descId',
    'name',
    'plural',
    'type',
    'outfit',
    'outfitId',
    'image',
    'power',
    'autosell',
    'npcPrice',
    'npcStoreId',
    'isUsable',
    'isMultiUsable',
    'isCombatUsable',
    'isReusable',
    'isCombatReusable',
    'isUsableOnOthers',
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
    'quality',
    'adventuresGained',
    'muscleGained',
    'mysticalityGained',
    'moxieGained',
    'numPackageItems',
    'isZappable',
    'isFoldable',
    'isBounty',
    'isCandy',
    'isSphere',
    'enchantments',
]

ITEM_ENCHANTMENTS = [
    'muscle',
    'mysticality',
    'moxie',
    'musclePercent',
    'mysticalityPercent',
    'moxiePercent',

    'adventuresAtRollover',
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

    'weaponDamage',
    'rangedDamage',
    'coldDamage',
    'hotDamage',
    'sleazeDamage',
    'spookyDamage',
    'stenchDamage',
    'spellDamage',
    'spellDamagePercent',

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

def writeItems(items, out):
    out.write("items = [\n")

    for item in items:
        out.write("    {\n")
        for attribute in ITEM_ATTRIBUTES:
            if attribute in item:

                # Skip trivial plurals.
                if attribute == "plural":
                    if item["plural"] == item["name"] + 's':
                        continue

                val = item[attribute]
                if type(val) == int or type(val) == bool:
                    out.write('        "%s" : %s,\n' % (attribute, val))
                elif type(val) == str:
                    out.write('        "%s" : "%s",\n' % (attribute, val))
                elif type(val) == list:
                    out.write('        "%s" : %s,\n' % (attribute, str(val)))
                elif attribute == "enchantments" and len(item["enchantments"]) > 0:
                    count = 0
                    for enchantment in ITEM_ENCHANTMENTS:
                        if enchantment in val:
                            count = count + 1

                    if count > 0:
                        out.write('        "%s" :\n' % attribute)
                        out.write('        {\n')
                        for enchantment in ITEM_ENCHANTMENTS:
                            if enchantment in val:
                                enVal = val[enchantment]
                                if type(enVal) == int or type(enVal) == bool:
                                    out.write('            "%s" : %s,\n' % (enchantment, enVal))
                                elif type(enVal) == str:
                                    out.write('            "%s" : "%s",\n' % (enchantment, enVal))
                                elif type(enVal) == list:
                                    out.write('            "%s" : %s,\n' % (enchantment, str(enVal)))
                        out.write('        },\n')
        out.write("    },\n")
    out.write(']\n')
