pykol
=====

The purpose of pykol is to create a [Python](http://www.python.org/)
package that makes it extremely easy to develop code that works with 
[The Kingdom of Loathing](http://www.kingdomofloathing.com). 

Example
-------
The following is some example code that depicts how to login to The Kingdom
of Loathing, grab the contents of your inbox, access the item database, as
well as use and smash items.

	from kol.Session import Session
	from kol.database import ItemDatabase
	from kol.request.GetMessagesRequest import GetMessagesRequest
	from kol.request.PulverizeRequest import PulverizeRequest
	
	# Login to the KoL servers.
	s = Session()
	s.login("myUserName", "myPassword")
	
	# Get a list of your kmails and print them out.
	r = GetMessagesRequest(s)
	responseData = r.doRequest()
	kmails = responseData["kmails"]
	for kmail in kmails:
		print "Received kmail from %s (#%s)" % (kmail["userName"], kmail["userId"])
		print "Text: %s" % kmail["text"]
		print "Meat: %s" % kmail["meat"]
		for item in kmail["items"]:
			print "Item: %s (%s)" % (item["name"], item["quantity"])
	
	# Use an old coin purse.
	item = ItemDatabase.getItemFromName("old coin purse")
	r = UseItemRequest(s, item["id"])
	r.doRequest()
	
	# Smash a titanium assault umbrella and print out the results.
	item = ItemDatabase.getItemFromName("titanium assault umbrella")
	r = PulverizeRequest(s, item["id"])
	responseData = r.doRequest()
	smashResults = responseData["results"]
	print "After smashing the item you have received the following:"
	for result in smashResults:
		print "%s (%s)" % (result["name"], result["quantity"])
	
	# Now we logout.
	s.logout()

Dependencies
------------
pykol requires Python 2.5 or higher. It does not require any third-party
libraries, however it does use a number of libraries that ship with the
standard distribution of Python.
