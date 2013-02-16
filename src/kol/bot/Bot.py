import BotManager
import BotUtils
import kol.Error as Error
from kol.Session import Session
from kol.database import ItemDatabase
from kol.manager import FilterManager
from kol.manager.ChatManager import ChatManager
from kol.manager.MailboxManager import MailboxManager
from kol.request.DeleteMessagesRequest import DeleteMessagesRequest
from kol.request.GetMessagesRequest import GetMessagesRequest
from kol.request.MainMapRequest import MainMapRequest
from kol.request.SendMessageRequest import SendMessageRequest
from kol.util import DataUtils
from kol.util import Report

import httplib
import os
import pickle
import threading
import time
import urllib2

COMMANDS_COMMANDS = ["command", "commands"]
HELP_COMMANDS = ["help"]
IGNORE_COMMANDS = ["ignore"]

class Bot(threading.Thread):
    """
    A Kingdom of Loathing bot. By itself, this module does very little. Instead, it provides
    filter hooks so that a real bot can be created just by implementing a few of them. The Bot
    class extends threading.Thread so that many bots can be created and managed by a module such
    as kol.bot.BotManager.

    One important aspect of this Bot to understand is state management. There are a number of
    "state files" which are created and used by the bot. These state files are used to hold
    information about what the bot is currently doing. They are designed so that if the bot
    crashes at any time (or if the Kingdom of Loathing servers go down), the bot can be started
    up again and continue right where it left off, thus minimizing the potential for data loss.
    """
    def __init__(self, params):
        super(Bot, self).__init__()

        self.params = params
        self.id = params["userName"]
        self.stateIds = ["global", "rollover", "cycle", "job", "kmail"]
        self.states = {}
        self.session = None
        self.runBot = True

        # Allow for people to hook in before the bot is initialized.
        self.executeFilter("botPreInitialization")

        # Load the current state of the bot.
        self.loadState()

        # Allow for people to hook in after the bot is initialized.
        self.executeFilter("botPostInitialization")

    def executeFilter(self, filterName, context=None, **kwargs):
        """
        This method will execute the specified filter after appending ':$botId' to the filterName.
        This allows the FilterManager to first execute this filter and then the filter with just
        the specified filterName. The purpose behind this is to let an application with multiple
        bots only assign some filters to particular bots instead of all of them. In addition,
        we almost always want to pass the bot itself along to the filter. This method will handle
        that for you.
        """
        if context == None:
            context = {}

        kwargs["bot"] = self
        return FilterManager.executeFiltersForEvent("%s:%s" % (filterName, self.id), context, **kwargs)

    def loadState(self):
        """
        Loads the state of the bot from files created through the pickle module. If any files
        are not found, that particular state object is set to an empty dictionary. Multiple
        state files are important so that different aspects of the bot can be stored in different
        files, thus making it easier to clean up the state by deleting a particular file.
        """
        for stateId in self.stateIds:
            path = "state_%s_%s.pkl" % (self.id, stateId)
            if os.path.exists(path):
                f = open(path, 'rb')
                self.states[stateId] = pickle.load(f)
                f.close()
            else:
                self.states[stateId] = {}

    def clearState(self, stateId):
        "Clears one of the bot's state files and objects."
        self.states[stateId] = {}
        path = "state_%s_%s.pkl" % (self.id, stateId)
        if os.path.exists(path):
            os.remove(path)

    def writeState(self, stateId):
        "Writes one of the bot's state files to disk."
        path = "state_%s_%s.pkl" % (self.id, stateId)
        f = open(path, 'wb')
        pickle.dump(self.states[stateId], f)
        f.close()

    def run(self):
        # Create a thread lock and set the thread name. This allows other bots to interact with
        # this bot and ensure that they are not doing work while this bot is in the middle of
        # a work cycle.
        self.lock = threading.Lock()
        threading.currentThread().setName(self.id)

        self.executeFilter("botStartup")

        while self.runBot:
            self.lock.acquire()
            try:
                state = self.states["cycle"]
                timeToSleep = DataUtils.getInteger(self.params, "timeToSleep", 30)

                try:
                    # Check to see how close we are to rollover. If we are within 5 minutes we should
                    # logout and then sleep for 10 minutes.
                    nowstruct = time.gmtime()
                    if nowstruct.tm_hour == 3 and nowstruct.tm_min >= 25 and nowstruct.tm_min <= 34:
                        Report.info("bot", "Rollover approaching.")
                        self.logout()
                        timeToSleep = 600
                    else:
                        # If necessary, login to the server.
                        if self.session == None or self.session.isConnected == False:
                            self.login()

                        # Set the current time as the beginTime for this cycle. We don't write the
                        # state immediately. We only write it once we get our work.
                        if "beginTime" not in state:
                            state["beginTime"] = int(time.time())
                        state["cycleBegun"] = True

                        # Allow for people to hook in at the beginning of a cycle.
                        self.executeFilter("botBeginCycle")

                        self.getWork()
                        self.doWork()
                        self.clearWork()

                        # Allow for people to hook in at the end of a cycle.
                        self.executeFilter("botEndCycle")

                        # If we have gotten this far, we have finished the processing cycle
                        # successfully. Reset our current state.
                        self.clearState("cycle")

                except Error.Error, inst:
                    msg = inst.msg
                    level = Report.WARNING
                    if inst.code == Error.NIGHTLY_MAINTENANCE:
                        timeToSleep = 300
                    elif inst.code == Error.LOGIN_FAILED_GENERIC:
                        level = Report.ERROR
                        timeToSleep = inst.timeToWait
                    elif inst.code == Error.NOT_LOGGED_IN:
                        timeToSleep = 600
                    else:
                        cxt = {}
                        self.executeFilter("botStandardException", cxt, inst=inst)
                        if "timeToSleep" in cxt:
                            timeToSleep = cxt["timeToSleep"]
                        if "level" in cxt:
                            level = cxt["level"]
                        else:
                            level = Report.FATAL
                    Report.report("bot", level, msg, inst)
                    if level == Report.FATAL:
                        self.prepareShutdown()
                except urllib2.URLError, inst:
                    Report.error("bot", "URLError! Let's try logging in again and maybe get a new server in the process.", inst)
                    self.session = None
                    timeToSleep = 120
                except httplib.BadStatusLine, inst:
                    Report.error("bot", "Bad HTTP Status! Let's try logging in again and maybe get a new server in the process.", inst)
                    self.session = None
                    timeToSleep = 120
                except Exception, inst:
                    Report.error("bot", "Unknown error.", inst)
                    cxt = {}
                    self.executeFilter("botUnknownException", cxt, inst=inst)
                    if "timeToSleep" in cxt:
                        timeToSleep = cxt["timeToSleep"]
                    else:
                        self.prepareShutdown()

            finally:
                # The cycle is over. Release the lock.
                self.lock.release()

            # Sleep until our next cycle.
            if self.runBot:
                Report.trace("bot", "Sleeping for %s seconds." % timeToSleep)
                BotManager._haltEvent.wait(timeToSleep)
                if BotManager._haltEvent.isSet():
                    self.runBot = False

        # Time to shutdown the bot.
        self.logout()
        self.executeFilter("botShutdown")

    def prepareShutdown(self):
        self.runBot = False
        BotManager._haltEvent.set()

    def login(self):
        "Logs in to the Kingdom of Loathing."
        self.executeFilter("botPreLogin")

        # Create the KoL Session.
        self.session = Session()
        Report.info("bot", "Logging in.")
        self.session.login(self.params["userName"], self.params["userPassword"])

        # Open the main map to clear the bot's alerts.
        r = MainMapRequest(self.session)
        r.doRequest()

        # Determine when next rollover happens, in UTC unix time format
        nextRollover = self.session.rollover

        # Clear rollover state if it is a different KoL day than last session
        if "expires" in self.states["rollover"]:
            rolloverTimeDiff = abs(nextRollover - self.states["rollover"]["expires"])
            if rolloverTimeDiff >= 12*60*60:  # half a day
                self.executeFilter("botPreClearRollover")
                self.clearState("rollover")

        # Set rollover state to be cleared next rollover
        self.states["rollover"]["expires"] = nextRollover

        # Create a MailboxManager.
        if "doWork:kmail" in self.params:
            m = MailboxManager(self.session)
            m.setMessagesPerPage(100)
            m.setOldestFirst(True)

        # Create a ChatManager.
        if "doWork:chat" in self.params:
            c = ChatManager(self.session)

        self.executeFilter("botPostLogin")

    def logout(self):
        "Logs out from the Kingdom of Loathing."
        if self.session != None and self.session.isConnected:
            self.executeFilter("botPreLogout")
            Report.info("bot", "Logging out.")
            self.session.logout()
            self.executeFilter("botPostLogout")

    def getWork(self):
        """
        Retrieves all of the work the bot needs to do during this cycle. Currently both chat
        messages and kmails can be used as work objects. In order to set which ones your bot
        should retrieve, make sure to set "doWork:kmail" and/or "doWork:chat" in the parameters
        of your bot.
        """
        state = self.states["cycle"]

        if "retrievedWork" not in state:
            if DataUtils.getBoolean(self.params, "doWork:kmail", False) and "kmails" not in state:
                Report.trace("bot", "Getting kmails.")
                messages = self.session.mailboxManager.getAllMessages(box="Inbox", openGiftPackages=True, removeGiftPackages=True)
                Report.trace("bot", "Retrieved %s kmails." % len(messages))
                state["kmails"] = messages
                self.writeState("cycle")

            if DataUtils.getBoolean(self.params, "doWork:chat", False) and "chatMessages" not in state:
                Report.trace("bot", "Getting chat messages.")
                chats = self.session.chatManager.getNewChatMessages()
                Report.trace("bot", "Retrieved %s chat messages." % len(chats))
                state["chats"] = chats
                self.writeState("cycle")

            state["retrievedWork"] = 1
            self.writeState("cycle")

    def doWork(self):
        """
        This is the method that actually does all of work for the bot. It can iterate through
        kmails or chat messages and then act on each one.
        """
        state = self.states["cycle"]

        if DataUtils.getBoolean(self.params, "doWork:kmail", False) and "kmails" in state:
            kmails = state["kmails"]
            if len(kmails) > 0:
                Report.info("bot", "Processing %s kmails." % len(kmails))
            while len(kmails) > 0:
                m = kmails[0]

                # Log the kmail.
                Report.info("bot", "Received kmail %s from %s (#%s)" % (m["id"], m["userName"], m["userId"]))
                Report.info("bot", "Text: %s" % m["text"])
                Report.info("bot", "Meat: %s" % m["meat"])
                for item in m["items"]:
                    Report.info("bot", "Item: %s (%s)" % (item["name"], item["quantity"]))

                # Allow for a filter to preprocess the kmail.
                self.executeFilter("botPreProcessKmail", None, kmail=m)

                try:
                    handledKmail = False

                    # Allow a filter to process the kmail.
                    returnCode = self.executeFilter("botProcessKmail", None, kmail=m)
                    if returnCode == FilterManager.FINISHED:
                        handledKmail = True

                    # See if we can handle the kmail ourselves.
                    if handledKmail == False:
                        cmd = BotUtils.getKmailCommand(m)
                        if cmd in HELP_COMMANDS and "helpKmailResponse" in self.params:
                            resp = {"userId":m["userId"], "text":self.params["helpKmailResponse"]}
                            self.sendKmail(resp)
                            handledKmail = True
                        elif cmd in COMMANDS_COMMANDS and "commandsKmailResponse" in self.params:
                            resp = {"userId":m["userId"], "text":self.params["commandsKmailResponse"]}
                            self.sendKmail(resp)
                            handledKmail = True
                        elif cmd in IGNORE_COMMANDS or m["messageType"] != "normal":
                            Report.info("bot", "Ignoring kmail.")
                            handledKmail = True

                    # If we could not handle the kmail, tell the user that we did not understand
                    # their request.
                    if handledKmail == False and "didNotUnderstandKmailResponse" in self.params:
                        self.returnKmail(m, self.params["didNotUnderstandKmailResponse"])
                        handledKmail = True

                except Error.Error, inst:
                    if inst.code == Error.BOT_REQUEST:
                        Report.info("bot", "Invalid kmail request.", inst)
                        self.returnKmail(m, inst.msg)
                    else:
                        raise inst

                # We are done with this kmail. Clean up the state and write it out.
                if "processedKmails" in state:
                    state["processedKmails"].append(kmails[0])
                else:
                    state["processedKmails"] = [kmails[0]]
                del kmails[0]
                self.writeState("cycle")
                self.clearState("job")

        if DataUtils.getBoolean(self.params, "doWork:chat", False) and "chats" in state:
            chats = state["chats"]
            if len(chats) > 0:
                Report.trace("bot", "Processing %s chat messages." % len(chats))
            while len(chats) > 0:
                chat = chats[0]

                # If this was a private chat message, log it.
                if chat["type"] == "private":
                    Report.info("bot", "Received private chat: %s" % chat)

                # Allow for a filter to preprocess the chat.
                self.executeFilter("botPreProcessChat", None, chat=chat)

                try:
                    handledChat = False

                    # Allow for a filter to process the chat command.
                    returnCode = self.executeFilter("botProcessChat", None, chat=chat)
                    if returnCode == FilterManager.FINISHED:
                        handledChat = True

                    # See if we can handle the chat ourselves.
                    if handledChat == False and chat["type"] == "private":
                        text = chat["text"]
                        if text.lower().find("help") == 0 or text == '?':
                            if "helpChatResponse" in self.params:
                                response = "/w %s %s" % (chat["userId"], self.params["helpChatResponse"])
                                self.sendChatMessage(response)
                                handledChat = True

                    # If we could not handle the chat, tell the user that we did not understand
                    # their request.
                    if handledChat == False and chat["type"] == "private":
                        if "didNotUnderstandChatResponse" in self.params:
                            response = "/w %s %s" % (chat["userId"], self.params["didNotUnderstandChatResponse"])
                            self.sendChatMessage(response)
                            handledChat = True

                    # Also allow bots to respond to chats with a kmail.
                    if handledChat == False and chat["type"] == "private":
                        if "didNotUnderstandChatResponseAsKmail" in self.params:
                            resp = {"userId":chat["userId"]}
                            resp["text"] = self.params["didNotUnderstandChatResponseAsKmail"]
                            self.sendKmail(resp)
                            handledChat = True

                except Error.Error, inst:
                    if inst.code == Error.BOT_REQUEST:
                        Report.info("bot", "Invalid chat request.", inst)
                        self.sendChatMessage(inst.msg)
                    else:
                        raise inst

                # We are done with this chat. Clean up the state and write it out.
                del chats[0]
                self.writeState("cycle")
                self.clearState("job")

    def clearWork(self):
        """
        Once the bot has processed all of its work for this cycle, this method will perform
        any necessary cleanup. If kmails were processed, delete them from the bot's inbox.
        """
        state = self.states["cycle"]
        if "doWork:kmail" in self.params and "processedKmails" in state:
            messages = state["processedKmails"]

            # If we have more than 100 kmails to delete, break them up into chunks.
            while len(messages) > 100:
                msgIds = []
                for i in range(100):
                    msgIds.append(messages[i]["id"])
                Report.info("bot", "Deleting %s kmails." % len(msgIds))
                r = DeleteMessagesRequest(self.session, msgIds)
                r.doRequest()
                Report.info("bot", "Kmails deleted.")
                messages = messages[100:]
                state["processedKmails"] = messages
                self.writeState("cycle")

            # Delete the remaining kmails.
            msgIds = []
            for m in messages:
                msgIds.append(m["id"])
            Report.info("bot", "Deleting %s kmails." % len(msgIds))
            r = DeleteMessagesRequest(self.session, msgIds)
            r.doRequest()
            Report.info("bot", "Kmails deleted.")

            del state["processedKmails"]
            self.writeState("cycle")

    def returnKmail(self, message, introText):
        m = {"userId":message["userId"], "meat":message["meat"], "items":message["items"]}
        m["text"] = introText + "\n\nOriginalMessage:\n--------------------\n" + message["text"]
        self.sendKmail(m)

    def quoteKmail(self, message, newText):
        m = {"userId":message["userId"]}
        m["text"] = newText + "\n\nOriginalMessage:\n--------------------\n" + message["text"]
        self.sendKmail(m)

    def sendKmail(self, m):
        """
        Sends a kmail to a user. This method is complicated because many bots need to be
        transactional with respect to sending kmails, especially when the bots are sending
        items or meat to other users. This method provides such functionality and allows
        for filters to modify and refine its behavior.
        """
        state = self.states["kmail"]

        # If we were interrupted, see if the message was actually sent.
        if "attemptingToSendMessage" in state and "sentMessageId" not in state:
            Report.warning("bot", "We were interrupted while attempting to send a kmail. Check to see if the message was sent.")
            r = GetMessagesRequest(self.session, box="Outbox")
            responseData = r.doRequest()
            messages = responseData["kmails"]
            if len(messages) > 0:
                state["sentMessage"] = 1
                state["sentMessageId"] = messages[0]["id"]
                self.writeState("kmail")
                Report.warning("bot", "Found sent message: %s" % state["sentMessageId"])
        else:
            state["attemptingToSendMessage"] = 1
            self.writeState("kmail")

        # Here we try to actually send the message.
        if "sentMessage" not in state:

            # Log the message we are sending
            Report.info("bot", "Sending message to %s." % m["userId"])
            Report.info("bot", "Text: %s" % m["text"])
            if "meat" in m and m["meat"] > 0:
                Report.info("bot", "Meat: %s" % m["meat"])
            if "items" in m and len(m["items"]) > 0:
                for item in m["items"]:
                    fullItem = ItemDatabase.getItemFromId(item["id"])
                    Report.info("bot", "Item: %s (%s)" % (fullItem["name"], item["quantity"]))

            # Send the message
            r = SendMessageRequest(self.session, m)
            try:
                r.doRequest()
                Report.info("bot", "Message sent.")
                state["sentMessage"] = 1
            except Error.Error, inst:
                if inst.code == Error.USER_IN_HARDCORE_RONIN:
                    Report.info("bot", "User could not receive items/meat.", inst)
                    state["userInHardcoreOrRonin"] = 1
                elif inst.code == Error.USER_IS_IGNORING:
                    Report.info("bot", "The user is ignorning us or we are ignoring them.", inst)
                    state["userIsIgnoringUs"] = 1
                else:
                    raise inst
                self.writeState("kmail")

        cxt = {}
        self.executeFilter("botPostAttemptSendKmail", cxt, kmail=m)

        if "userInHardcoreOrRonin" in state and "ignoreErrors" not in cxt:
            self.clearState("kmail")
            raise Error.Error("User is unable to receive items or meat.", Error.USER_IN_HARDCORE_RONIN)

        if "userIsIgnoringUs" in state and "ignoreErrors" not in cxt:
            self.clearState("kmail")
            raise Error.Error("User is ignoring us.", Error.USER_IS_IGNORING)

        # Grab the sent message to delete.
        if "sentMessage" in state and "sentMessageId" not in state:
            Report.trace("bot", "Looking for sent message.")
            r = GetMessagesRequest(self.session, box="Outbox")
            responseData = r.doRequest()
            messages = responseData["kmails"]
            if len(messages) > 0:
                state["sentMessageId"] = messages[0]["id"]
                Report.trace("bot", "Found sent message: %s" % state["sentMessageId"])
                self.writeState("kmail")
            else:
                del state["sentMessage"]
                self.writeState("kmail")
                Report.fatal("bot", "Crap! Message was not sent. Bailing out.")
                raise Error.Error("We thought we sent a message but didn't. Uh oh!", Error.REQUEST_GENERIC)

        # Delete the sent message
        if "sentMessageId" in state:
            Report.trace("bot", "Deleting message in outbox.")
            r = DeleteMessagesRequest(self.session, [state["sentMessageId"]], box="Outbox")
            r.doRequest()
            Report.trace("bot", "Message deleted.")

        # Update our state. We are done sending the message, so we can remove all of the
        # message-specific keys.
        self.clearState("kmail")

    def sendChatMessage(self, chat):
        "Sends a chat message to the KoL server."
        Report.info("bot", "Sending chat: %s" % chat)
        return self.session.chatManager.sendChatMessage(chat)
