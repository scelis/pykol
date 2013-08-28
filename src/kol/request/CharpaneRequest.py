from GenericRequest import GenericRequest
from kol.manager import PatternManager

class CharpaneRequest(GenericRequest):
    "Requests the user's character pane."

    def __init__(self, session):
        super(CharpaneRequest, self).__init__(session)
        self.url = session.serverURL + 'charpane.php'

    def parseResponse(self):
        accountPwdPattern = PatternManager.getOrCompilePattern('accountPwd')
        match = accountPwdPattern.search(self.responseText)
        self.responseData["pwd"] = match.group(1)

        accountNamePattern = PatternManager.getOrCompilePattern('accountName')
        match = accountNamePattern.search(self.responseText)
        self.responseData["userName"] = match.group(1)

        accountIdPattern = PatternManager.getOrCompilePattern('accountId')
        match = accountIdPattern.search(self.responseText)
        self.responseData["userId"] = int(match.group(1))

        characterLevelPattern = PatternManager.getOrCompilePattern('characterLevel')
        match = characterLevelPattern.search(self.responseText)
        if match:
            self.responseData["level"] = int(match.group(1))
            title = str(match.group(2))
            self.responseData["levelTitle"] = title
            if title == "Astral Spirit":
                self.responseData["class"] = "Astral Spirit"
            elif title in ["Lemming Trampler", "Tern Slapper", "Puffin Intimidator", "Ermine Thumper", "Penguin Frightener", "Malamute Basher", "Narwhal Pummeler", "Otter Crusher", "Caribou Smacker", "Moose Harasser", "Reindeer Threatener", "Ox Wrestler", "Walrus Bludgeoner", "Whale Boxer", "Seal Clubber"]:
                self.responseData["class"] = "Seal Clubber"
            elif title in ["Toad Coach", "Skink Trainer", "Frog Director", "Gecko Supervisor", "Newt Herder", "Frog Boss", "Iguana Driver", "Salamander Subduer", "Bullfrog Overseer", "Rattlesnake Chief", "Crocodile Lord", "Cobra Commander", "Alligator Subjugator", "Asp Master", "Turtle Tamer"]:
                self.responseData["class"] = "Turtle Tamer"
            elif title in ["Dough Acolyte", "Yeast Scholar", "Noodle Neophyte", "Starch Savant", "Carbohydrate Cognoscenti", "Spaghetti Sage", "Macaroni Magician", "Vermicelli Enchanter", "Linguini Thaumaturge", "Ravioli Sorcerer", "Manicotti Magus", "Spaghetti Spellbinder", "Cannelloni Conjurer", "Angel-Hair Archmage", "Pastamancer"]:
                self.responseData["class"] = "Pastamancer"
            elif title in ["Allspice Acolyte", "Cilantro Seer", "Parsley Enchanter", "Sage Sage", "Rosemary Diviner", "Thyme Wizard", "Tarragon Thaumaturge", "Oreganoccultist", "Basillusionist", "Coriander Conjurer", "Bay Leaf Brujo", "Sesame Soothsayer", "Marinara Mage", "Alfredo Archmage", "Sauceror"]:
                self.responseData["class"] = "Sauceror"
            elif title in ["Funk Footpad", "Rhythm Rogue", "Chill Crook", "Jiggy Grifter", "Beat Snatcher", "Sample Swindler", "Move Buster", "Jam Horker", "Groove Filcher", "Vibe Robber", "Boogie Brigand", "Flow Purloiner", "Jive Pillager", "Rhymer And Stealer", "Disco Bandit"]:
                self.responseData["class"] = "Disco Bandit"
            elif title in ["Polka Criminal", "Mariachi Larcenist", "Zydeco Rogue", "Chord Horker", "Chromatic Crook", "Squeezebox Scoundrel", "Concertina Con Artist", "Button Box Burglar", "Hurdy-Gurdy Hooligan", "Sub-Sub-Apprentice Accordion Thief", "Sub-Apprentice Accordion Thief", "Pseudo-Apprentice Accordion Thief", "Hemi-Apprentice Accordion Thief", "Apprentice Accordion Thief", "Accordion Thief"]:
                self.responseData["class"] = "Accordion Thief"

        characterHPPattern = PatternManager.getOrCompilePattern('characterHP')
        match = characterHPPattern.search(self.responseText)
        if match:
            self.responseData["currentHP"] = int(match.group(1))
            self.responseData["maxHP"] = int(match.group(2))

        characterMPPattern = PatternManager.getOrCompilePattern('characterMP')
        match = characterMPPattern.search(self.responseText)
        if match:
            self.responseData["currentMP"] = int(match.group(1))
            self.responseData["maxMP"] = int(match.group(2))

        characterMeatPattern = PatternManager.getOrCompilePattern('characterMeat')
        match = characterMeatPattern.search(self.responseText)
        if match:
            self.responseData["meat"] = int(match.group(1).replace(',', ''))

        characterAdventuresPattern = PatternManager.getOrCompilePattern('characterAdventures')
        match = characterAdventuresPattern.search(self.responseText)
        if match:
            self.responseData["adventures"] = int(match.group(1))

        characterDrunkPattern = PatternManager.getOrCompilePattern('characterDrunk')
        match = characterDrunkPattern.search(self.responseText)
        if match:
            self.responseData["drunkenness"] = int(match.group(1))

        currentFamiliarPattern = PatternManager.getOrCompilePattern('currentFamiliar')
        match = currentFamiliarPattern.search(self.responseText)
        if match:
            self.responseData["familiar"] = {'name':str(match.group(1)), 'type':str(match.group(3)), 'weight':int(match.group(2))}

        effects = []
        characterEffectPattern = PatternManager.getOrCompilePattern('characterEffect')
        for match in characterEffectPattern.finditer(self.responseText):
            effect = {}
            effect["name"] = str(match.group(1))
            effect["turns"] = int(match.group(2))
            effects.append(effect)
        if len(effects) > 0:
            self.responseData["effects"] = effects

        characterMusclePattern = PatternManager.getOrCompilePattern('characterMuscle')
        match = characterMusclePattern.search(self.responseText)
        if match:
            if match.group(1) and len(str(match.group(1))) > 0:
                self.responseData["buffedMuscle"] = int(match.group(1))
            self.responseData["baseMuscle"] = int(match.group(2))

        characterMoxiePattern = PatternManager.getOrCompilePattern('characterMoxie')
        match = characterMoxiePattern.search(self.responseText)
        if match:
            if match.group(1) and len(str(match.group(1))) > 0:
                self.responseData["buffedMoxie"] = int(match.group(1))
            self.responseData["baseMoxie"] = int(match.group(2))

        characterMysticalityPattern = PatternManager.getOrCompilePattern('characterMysticality')
        match = characterMysticalityPattern.search(self.responseText)
        if match:
            if match.group(1) and len(str(match.group(1))) > 0:
                self.responseData["buffedMysticality"] = int(match.group(1))
            self.responseData["baseMysticality"] = int(match.group(2))

        characterRoninPattern = PatternManager.getOrCompilePattern('characterRonin')
        match = characterRoninPattern.search(self.responseText)
        if match:
            self.responseData["roninLeft"] = int(match.group(1))

        characterMindControlPattern = PatternManager.getOrCompilePattern('characterMindControl')
        match = characterMindControlPattern.search(self.responseText)
        if match:
            self.responseData["mindControl"] = int(match.group(1))
