pykol
=====

What is it?
-----------
The purpose of pykol is to create a [Python](http://www.python.org/)
package that makes it extremely easy to develop code that works with
[The Kingdom of Loathing](http://www.kingdomofloathing.com). pykol can
be used for anything from writing short scripts to complex bots. In fact,
both [kBay](http://forums.kingdomofloathing.com:8080/vb/showthread.php?t=141613)
and [wadbot](http://forums.kingdomofloathing.com:8080/vb/showthread.php?t=152258)
are built completely on top of it.

Who is it for?
--------------
pykol is for programmers who are interested in writing scripts and bots
for KoL. If you do not feel comfortable writing code, then pykol is
probably not for you.

Example
-------
The following is some example code that demonstrates how to login to The Kingdom
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

Requirements
------------
pykol requires Python 2.5. It does not require any third-party libraries,
however it does use a number of libraries that ship with the standard
distribution of Python.

How can I contribute?
---------------------
1. [Fork](http://help.github.com/forking/) pykol
2. Clone your fork - `git clone git@github.com:your_username/pykol.git`
3. Add a remote to this repository - `git remote add upstream git://github.com/scelis/pykol.git`
4. Fetch the current pykol sources - `git fetch upstream`
5. Create a topic branch - `git checkout -b my_branch upstream/master`
6. Commit (or cherry-pick) your changes
7. Push your branch to github - `git push origin my_branch`
8. Create an [Issue](http://github.com/scelis/pykol/issues) with a link to your branch
9. That's it!
