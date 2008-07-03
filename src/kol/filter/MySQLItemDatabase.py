from kol.database import ItemDatabase
from kol.manager import FilterManager
from kol.manager import MySQLDatabaseManager

def doFilter(eventName, context, **kwargs):
	if eventName == "preInitializeItemDatabase":
		preInitializeItemDatabase(context, **kwargs)
	elif eventName == "discoveredNewItem":
		discoveredNewItem(context, **kwargs)

def preInitializeItemDatabase(context, **kwargs):
	db = MySQLDatabaseManager.getDatabase("system")
	c = db.cursor()
	c.execute("SELECT * FROM item")
	row = c.fetchone()
	while row != None:
		item = {}
		item["id"] = row["item_id"]
		item["descId"] = row["desc_id"]
		item["name"] = row["name"]
		item["image"] = row["image"]
		item["autosell"] = row["autosell"]
		item["type"] = row["type"]
		ItemDatabase.addItem(item)
		row = c.fetchone()
	c.close()
	context["returnCode"] = FilterManager.FINISHED

def discoveredNewItem(context, **kwargs):
	if "item" in kwargs:
		item = kwargs["item"]
		
		if "type" in item:
			itemType = item["type"]
		else:
			itemType = ""
		if "image" in item:
			image = item["image"]
		else:
			image = ""
		if "autosell" in item:
			autosell = item["autosell"]
		else:
			autosell = 0
		
		db = MySQLDatabaseManager.getDatabase("system")
		c = db.cursor()
		c.execute("INSERT INTO item (item_id, desc_id, name, image, autosell, type) values (%s, %s, %s, %s, %s, %s)", \
			(item["id"], item["descId"], item["name"], image, autosell, itemType))
		c.close()
		db.commit()
