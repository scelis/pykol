from kol.relay.RelayRequestHandler import RelayRequestHandler
from kol.util import Report

from BaseHTTPServer import HTTPServer
import os
import socket
import threading

class RelayServer(threading.Thread):
    """
    This class acts as a relay server, allowing users to use a browser to communicate with the KoL
    servers even if they are already logged in via a script or bot. It works much like the KoLmafia
    relay browser system by listening to a port on the local machine. Any traffic sent to that port
    will be relayed to the KoL servers. Eventually, the response will be sent back on the same
    socket.

    Note that if the port is already in use, this class will try again with the next highest port
    number. It will do this a total of 10 times before finally giving up and raising a socket.error
    exception.
    """

    def __init__(self, session, port=8557):
        super(RelayServer, self).__init__()
        self.session = session
        self.port = port
        self.haltEvent = threading.Event()

    def run(self):
        Report.trace('relay', 'Starting RelayServer on port %s...' % self.port)

        started = False
        numTries = 0
        while not started:
            try:
                server = HTTPServer(('', self.port), RelayRequestHandler)
                started = True
            except socket.error, inst:
                numTries += 1
                if numTries == 10:
                    raise inst
                Report.trace('relay', 'Could not listen on port %s. Trying %s instead.' % (self.port, self.port + 1))
                self.port += 1

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
