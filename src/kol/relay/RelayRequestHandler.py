from kol.request.DynamicRequest import DynamicRequest
from kol.util import Report

from BaseHTTPServer import BaseHTTPRequestHandler

class RelayRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if not self.path.count('/newchatmessages.php?') and not self.path.count('/submitnewchat.php?'):
            Report.debug("relay", "GET: %s" % self.path)

        relayServer = self.server.relayServer

        # Check to see if we should terminate the RelayServer.
        if self.path == '/terminate':
            relayServer.haltEvent.set()
            self.wfile.write('Server Stopping...')
            return

        # Redirect empty URL to main.html.
        if self.path == '/':
            self.path = '/main.html'

        # Execute the server request.
        dReq = DynamicRequest(relayServer.session, self.path[1:])
        dReq.doRequest()

        # The following line is for the sake of some js scripts (mainly chat).
        page = dReq.responseText.replace("window.location.hostname", 'window.location.hostname+":"+window.location.port')

        # Add server shutdown in compact mode.
        if self.path == '/topmenu.php':
            page = page.replace('<option value="logout.php">Log Out</option>','<option value="terminate">Stop Server</option>')

        self.wfile.write(page)

    def do_POST(self):
        Report.debug("relay", "POST: %s" % self.path)

        relayServer = self.server.relayServer

        # Parse out the POST parameters.
        headers = str(self.headers).split('\n')
        length = 0
        for x in headers:
            if x.split(':')[0].lower() == 'content-length':
                length = int(x.split(':')[1].strip())
        payload =  self.rfile.read(length)

        # Execute the server request.
        dReq = DynamicRequest(relayServer.session, self.path[1:], payload)
        dReq.doRequest()
        self.wfile.write(dReq.responseText)
