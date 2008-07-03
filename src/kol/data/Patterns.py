import re

patterns = {
	# General patterns.
	"whitespace" : r'([\t ]+)',
	"results" : r'<b>Results:<\/b><\/td><\/tr><tr><td[^<>]*><center><table><tr><td>(.*?)</td></tr></table></center></td></tr>',
	
	# Login-related patterns.
	"accountPwd" : r"name=\"?pwd\"? value='([0-9a-f]+)'",
	"accountUserNameAndId" : r"<b>([^<>]*)<\/b> ?\(#([0-9]+)\)<table",
	"badPassword" : r'<b>Login failed\. Bad password\.<\/b>',
	"loginChallenge" : r'name="?challenge"?\s+value="?([0-9a-f]+)"?',
	"loginURL" : r'^(.*)login\.php\?loginid=([0-9a-f]+)',
	"mainFrameset" : r'<frameset id="?rootset"?',
	"tooManyLoginsFailuresFromThisIP" : r'Too many login failures from this IP',
	"waitOneMinuteLoginError" : r'Too many login attempts in too short a span of time',
	"waitTwoMinutesLoginError" : r"Whoops -- it looks like you had a recent session open that didn't get logged out of properly\.",
	"waitFifteenMinutesLoginError" : r'Please wait fifteen minutes and try again\.',
	
	# Item-related patterns.
	"acquireSingleItem" : r"<td[^>]*><img [^>]*onClick='descitem\(([0-9]+)\)'[^>]*><\/td><td[^>]*>You acquire an item",
	"acquireMultipleItems" : r"<td[^>]*><img [^>]*onClick='descitem\(([0-9]+)\)'[^>]*><\/td><td[^>]*>You acquire <b>([0-9,]*) ",
	"gainMeat" : r'<td><img src="[^"]*meat\.gif"[^>]*><\/td><td[^>]*>You gain ([0-9,]*?) Meat\.<\/td>',
	"isCocktailcraftingIngredient" : (r'<br>\(Cocktailcrafting ingredient\)<br>'),
	"isCookingIngredient" : r'<br>\(Cooking ingredient\)<br>',
	"isJewelrymakingComponent" : r'<br>\(Jewelrymaking component\)<br>',
	"isMeatsmithingComponent" : r'<br>\(Meatsmithing component\)<br>',
	"inventorySingleItem" : r'<img [^>]*descitem\(([0-9]+)\)[^>]*></td><td valign=top><b>([^<>]+)</b> <',
	"inventoryMultipleItems" : r'<img [^>]*descitem\(([0-9]+)\)[^>]*></td><td valign=top><b>([^<>]+)</b>  \(([0-9]+)\)',
	"itemAutosell" : r'<br>Selling Price: <b>(\d*) Meat\.<\/b>',
	"itemImage" : r'<img src="http:\/\/images\.kingdomofloathing\.com\/itemimages\/(.*?)"',
	"itemName" : r'<br><b>([^<>]+)<\/b><p>',
	"itemType" : r'<br>Type: <b>([^<]*)<\/b><br>',
	
	# Message-related patterns.
	"brickMessage" : r"http:\/\/images\.kingdomofloathing\.com\/adventureimages\/(brokewin|bigbrick)\.gif",
	"candyHeartMessage" : r"http:\/\/images\.kingdomofloathing\.com\/otherimages\/heart\/hearttop\.gif",
	"coffeeMessage" : r"http:\/\/images\.kingdomofloathing\.com\/otherimages\/heart\/cuptop\.gif",
	"fullMessage" : ('<tr><td[^>]*><input type=checkbox name="sel([0-9]+)".*?<b>[^<]*<\/b> <a href="showplayer\.php\?who=([0-9]+)">([^<]*)<\/a>.*?<b>Date:<\/b>([^<]*?)</b>.*?<blockquote>(.*?)<\/blockquote>', re.DOTALL),
	"userInHardcoreRonin" : r'<center><table><tr><td>That player cannot receive Meat or items from other players right now\.',
	"userIgnoringUs" : r"<center><table><tr><td>This message could not be sent, because you are on that player's ignore list\.<\/td><\/tr><\/table><\/center>",
	
	# Error patterns.
	"cantPulverizeItem" : r"<td>That's not something you can pulverize\.<\/td>",
	"notEnoughItems" : r"<td>You haven't got that many\.<\/td>",
}
