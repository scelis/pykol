from kol.relay.RelayRequestHandler import RelayRequestHandler
from kol.util import Report

from BaseHTTPServer import HTTPServer
import os
import threading

class RelayServer(threading.Thread):
	def __init__(self, session, port=8557):
		super(RelayServer, self).__init__()
		self.session = session
		self.port = port
		self.haltEvent = threading.Event()
	
	def run(self):
		Report.trace('relay', 'Starting RelayServer on port %s...' % self.port)
		server = HTTPServer(('', 8557), RelayRequestHandler)
		server.relayServer = self
		Report.trace('relay', 'RelayServer started.')
		
		# Handle requests for as long as we can.
		while (not self.haltEvent.isSet()):
			server.handle_request()
		
		# Shut down the RelayServer.
		Report.trace('relay', 'Shutting down RelayServer.')
		server.socket.close()
		
	def launchRelayBrowser(self):
		"Launch the relay server URL in a browser window."
		url = 'http://localhost:%s/main.html' % self.port
		
		if os.name == 'nt':
			os.startfile(url)
		else:
			os.spawnlp(os.P_NOWAIT, "open", "open", url)
