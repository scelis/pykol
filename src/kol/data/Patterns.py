"""
This module holds all of the regular expression patterns that pykol uses. It makes sense
to store them all in the same place since many patterns are used by multiple requests.
The 'patterns' data object is a dictionary mapping patternId to pattern. If pattern is a tuple,
then the first element of the tuple should be the pattern while the second element is a flag
to pass to re.compile (like re.DOTALL).
"""

import re

patterns = {
	# General patterns.
	"whitespace" : r'([\t ]+)',
	"results" : r'<b>Results:<\/b><\/td><\/tr><tr><td[^<>]*><center><table><tr><td>(.*?)</td></tr></table></center></td></tr>',
	"htmlComment" : r'<!--.*?-->',
	"htmlTag" : r'<[^>]*?>',
	
	# Login-related patterns.
	"accountPwd" : r"name=\"?pwd\"? value='([0-9a-f]+)'",
	"accountUserNameAndId" : r"<b>([^<>]*)<\/b> ?\(#([0-9]+)\)<table",
	"badPassword" : r'<b>Login failed\. Bad password\.<\/b>',
	"loginChallenge" : r'name="?challenge"?\s+value="?([0-9a-f]+)"?',
	"loginURL" : r'^(.*)login\.php\?loginid=([0-9a-f]+)',
	"mainFrameset" : r'<frameset id="?rootset"?',
	"tooManyLoginsFailuresFromThisIP" : r'Too many login failures from this IP',
	"waitOneMinuteLoginError" : r'Please wait a minute',
	"waitTwoMinutesLoginError" : r"you'll need to wait a couple of minutes before you can log in again\.",
	"waitFifteenMinutesLoginError" : r'Please wait fifteen minutes and try again\.',
	
	# Item-related patterns.
	"acquireSingleItem" : r"<td[^>]*><img [^>]*onClick='descitem\(([0-9]+)\)'[^>]*><\/td><td[^>]*>You acquire an item",
	"acquireMultipleItems" : r"<td[^>]*><img [^>]*onClick='descitem\(([0-9]+)\)'[^>]*><\/td><td[^>]*>You acquire <b>([0-9,]*) ",
	"gainMeat" : r'<td><img src="[^"]*meat\.gif"[^>]*><\/td><td[^>]*>You gain ([0-9,]*?) Meat\.<\/td>',
	"loseMeat" : r'You lose ([0-9,]*?) Meat',
	"isCocktailcraftingIngredient" : (r'<br>\(Cocktailcrafting ingredient\)<br>'),
	"isCookingIngredient" : r'<br>\(Cooking ingredient\)<br>',
	"isJewelrymakingComponent" : r'<br>\(Jewelrymaking component\)<br>',
	"isMeatsmithingComponent" : r'<br>\(Meatsmithing component\)<br>',
	"inventorySingleItem" : r'<img [^>]*descitem\(([0-9]+)\)[^>]*></td><td valign=top><b>([^<>]+)</b> <',
	"inventoryMultipleItems" : r'<img [^>]*descitem\(([0-9]+)\)[^>]*></td><td valign=top><b>([^<>]+)</b>  \(([0-9]+)\)',
	"itemAutosell" : r'<br>Selling Price: <b>(\d*) Meat\.<\/b>',
	"itemImage" : r'<img src="http:\/\/images\.kingdomofloathing\.com\/itemimages\/(.*?)"',
	"itemName" : r'<b>([^<>]+?)<\/b>',
	"itemType" : r'<br>Type: <b>([^<]*)<\/b><br>',
	
	# Message-related patterns.
	"brickMessage" : r"http:\/\/images\.kingdomofloathing\.com\/adventureimages\/(brokewin|bigbrick)\.gif",
	"candyHeartMessage" : r"http:\/\/images\.kingdomofloathing\.com\/otherimages\/heart\/hearttop\.gif",
	"coffeeMessage" : r"http:\/\/images\.kingdomofloathing\.com\/otherimages\/heart\/cuptop\.gif",
	"fullMessage" : ('<tr><td[^>]*><input type=checkbox name="sel([0-9]+)".*?<b>[^<]*<\/b> <a href="showplayer\.php\?who=([0-9]+)">([^<]*)<\/a>.*?<b>Date:<\/b>([^<]*?)</b>.*?<blockquote>(.*?)<\/blockquote>', re.DOTALL),
	"userInHardcoreRonin" : r'<center><table><tr><td>That player cannot receive Meat or items from other players right now\.',
	"userIgnoringUs" : r"<center><table><tr><td>This message could not be sent, because you are on that player's ignore list\.<\/td><\/tr><\/table><\/center>",
	"notEnoughItemsToSend" : r"<center><table><tr><td>You don't have enough of one of the items you're trying to send\.<\/td><\/tr><\/table><\/center>",
	"messageSent" : r"<td><center>Message sent\.<\/center><\/td>",
	
	# Error patterns.
	"cantPulverizeItem" : r"<td>That's not something you can pulverize\.<\/td>",
	"notEnoughItems" : r"<td>You haven't got that many\.<\/td>",
	
	# Chat patterns.
	"currentChatChannel" : r'<font color="?#?\w+"?>Currently in channel: ([^<>]+)<',
	"chatLastSeen" : r"lastseen:([0-9]+)",
	"chatChannel" : r'^<font color="?#?\w+"?>\[([^<>]+)\]<\/font> ',
	"chatMessage" : r'<b><a target="?mainpane"? href="showplayer\.php\?who=(-?[0-9]+)"><font color="?#?\w+"?>([^<>]+)<\/font><\/b><\/a>: (.*)$',
	"chatEmote" : r'<b><i><a target="?mainpane"? href="showplayer\.php\?who=([0-9]+)"><font color="?#?\w+"?>([^<>]+)<\/b><\/font><\/a> (.*)<\/i>$',
	"privateChat" : r'<a target="?mainpane"? href="showplayer\.php\?who=([0-9]+)"><font color="?blue"?><b>([^)]+) \(private\):<\/b><\/a> (.*)</font>$',
	"chatNewKmailNotification" : r'<a target="?mainpane"? href="messages\.php"><font color="?green"?>New message received from <a target="?mainpane"? href=\'showplayer\.php\?who=([0-9]+)\'><font color="?green"?>([^<>]+)<\/font><\/a>\.<\/font><\/a>$',
	"chatLink" : r'<a target="?_blank"? href="([^"]+)"><font color="?blue"?>\[link\]<\/font><\/a> ',
	"chatWhoResponse" : r'<table><tr><td class=tiny><center><b>Players in this channel:',
	"chatWhoPerson" : r'<a target="?mainpane"? href="showplayer\.php\?who=([0-9]+)"><font color="?#?\w+"?>([^<>]+)<\/font><\/a>',
	"chatLinkedPlayer" : r"<a style='color: #?\w+' href='showplayer\.php\?who=([0-9]+)' target=mainpane>([^<]+)<\/a>",
	
	# Clan dungeon patterns.
	"dungeonActivity" : r'(?:^|<br>|<br><b>|<b>)([^<>]+) \(#([0-9,]+)\) ([^<>]+) \(([0-9,]+) turns?\)',
	"dungeonLootDistribution" : r'(?:<blockquote>|<br>)([^<>]+) \(#([0-9,]+)\) distributed <b>([^<>]+)</b> to ([^<>]+) \(#([0-9,]+)\)<br>',
	"dungeonPreviousRun" : r'<tr><td class="?small"?>([^<>]+)&nbsp;&nbsp;<\/td><td class="?small"?>([^<>]+)&nbsp;&nbsp;<\/td><td class="?small"?>([^<>]+)&nbsp;&nbsp;<\/td><td class="?small"?>([0-9,]+)<\/td><td class="?tiny"?>\[<a href="clan_raidlogs\.php\?viewlog=([0-9]+)">view logs<\/a>\]<\/td><\/tr>',
	"dungeonLogCategory" : r'<b>([^<>]+):<\/b><blockquote>(.*?)<\/blockquote>',
	"imprisonedByChums" : r'^(.*) has been imprisoned by the C\. H\. U\. M\.s!$',
	"freedFromChums" : r'^(.*) has rescued (.*) from the C\. H\. U\. M\.s\.$',
	
	# Cocktailcrafting patterns.
	"itemsDontMakeCocktail" : r"<td>Those two items don't combine to make a refreshing cocktail\.</td>",
	"dontHaveSkillToMixCocktail" : r"<td>You don't have the skill necessary to make that cocktail\.</td>",
	"dontHaveItemsForThatCocktail" : r"<td>You don't have enough of one of the necessary items to make a cocktail that tasty\.</td>",
	"dontHaveAdventuresToMixCocktail" : r"<td>You don't have that many adventures left\. +It takes <i>time<\/i> to make a good cocktail, man\.</td>",
	
	# Character Pane patterns.
	'characterLevel' : r'<br>Level ([0-9]+)<br>(.*?)<table',
	'characterMuscle' : r'Muscle:</td><td align=left><b>(?:<font color=blue>([0-9]+)</font>)?(?:&nbsp;)?\(?([0-9]+)\)?</b>',
	'characterMoxie' : r'Moxie:</td><td align=left><b>(?:<font color=blue>([0-9]+)</font>)?(?:&nbsp;)?\(?([0-9]+)\)?</b>',
	'characterMysticality' : r'Mysticality:</td><td align=left><b>(?:<font color=blue>([0-9]+)</font>)?(?:&nbsp;)?\(?([0-9]+)\)?</b>',
	'characterHP' : r'onclick=\'doc\("hp"\);\'><br><span class=black>([0-9]+)&nbsp;/&nbsp;([0-9]+)</span>',
	'characterMP' : r'onclick=\'doc\("mp"\);\'><br><span class=black>([0-9]+)&nbsp;/&nbsp;([0-9]+)</span>',
	'characterMeat' : r'onclick=\'doc\("meat"\);\'><br><span class=black>([0-9,]+)</span>',
	'characterAdventures' : r'onclick=\'doc\("adventures"\);\'><br><span class=black>([0-9]+)</span>',
	'currentFamiliar' : r'href="familiar.php">(?:<b>)?<font size=[0-9]+>(.*?)</a>(?:</b>)?, the  ([0-9]+)-pound (.*?)<table',
	'characterEffect' : r'eff\("[a-fA-F0-9]+"\);\'.*?></td><td valign=center><font size=[0-9]+>(.*?) ?\(([0-9]+)\)</font><br></td>',
	
	# Stat, Substat, Leveling, HP, and MP patterns. Will fail in Haiku Dungeon.
	'muscleGainLoss' : r'You (gain|lose) ([0-9,]+) (?:Beefiness|Fortitude|Muscleboundness|Strengthliness|Strongness)',
	'mysticalityGainLoss' : r'You (gain|lose) ([0-9,]+) (?:Enchantedness|Magicalness|Mysteriousness|Wizardliness)',
	'moxieGainLoss' : r'You (gain|lose) ([0-9,]+) (?:Cheek|Chutzpah|Roguishness|Sarcasm|Smarm)',
	'musclePointGainLoss' : r'You (gain|lose) (?:a|some) Muscle points?',
	'mystPointGainLoss' : r'You (gain|lose) (?:a|some) Mysticality points?',
	'moxiePointGainLoss' : r'You (gain|lose) (?:a|some) Moxie points?',
	'levelGain' : r'You gain (?:(?:a)|(?:some)) (?:L|l)evels?',
	'hpGainLoss' : r'You (gain|lose) ([0-9,]+) hit points?',
	'mpGainLoss' : r'You (gain|lose) ([0-9,]+) (?:Muscularity|Mana|Mojo) (?:P|p)oints?',
	
	# Drunkenness, Adventures, and Effect patterns.
	'gainDrunk' : r'You gain ([0-9]+) Drunkenness',
	'gainAdventures' : r'You gain ([0-9,]+) Adventures',
	'gainEffect' : r'<td valign=center class=effect>You acquire an effect: <b>(.*?)</b><br>\(duration: ([0-9,]+) Adventures\)</td>',
	
	# Meatpasting patterns.
	'noMeatpaste' : (r"<b>Results:</b>.*You don't have any meat paste.*<b>Combine Items:</b>", re.DOTALL),
	'itemsDontMeatpaste' : r"<td>Those two items don't combine to make anything interesting\.</td>",
	'dontHaveItemsMeatpaste' : r"<td>You don't have enough of one the necessary items to make that combination\.</td>",
	'noMeatForMeatpasting' : r"<td>You don't have enough Meat to make that many\.</td>",
	
	# Store patterns.
	'meatSpent' : r'You spent ([0-9,]+) Meat',
	'noMeatForStore' : r"(?:You can't afford that many of that item)|(?:You can't afford that item)",
	'invalidStore' : r"You've been sent back here by some kind of bug",
	'notSoldHere' : r"This store doesn't sell that item",

	# Hermit patterns.
	'noTrinkets' : r"You don't have enough stuff",
	#'noHermitPermits' : r'',
	'notEnoughClovers' : r"you are able to infer that he doesn't have enough clovers to make that trade",
	
	# Adventure patterns.
	"twiddlingThumbs" : r"You twiddle your thumbs\.",
	"userShouldNotBeHere" : r">You shouldn't be here\.<",
	"monsterName" : r"<span id='monname'>(.*?)<\/span>",
	"choiceIdentifier" : r'<input type="?hidden"? name="?whichchoice"? value="?([0-9]+)"?>',
	"choiceName" : r"<b>([^<>]+?)<\/b><\/td><\/tr>",
	"noncombatName" : r"<center><table><tr><td><center><b>([^<>]+)<\/b><br><img",
	"fightWon" : r"<center>You win the fight!<!--WINWINWIN--><p>",
	"fightLost" : r"<p>You lose\. +You slink away, dejected and defeated\.<p>",
	
	# Rumpus Room Patterns
	'rumpusRoom' : r'rump([0-9])_([0-9])\.gif',
}
