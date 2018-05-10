import logging
import socket
import sys
import threading
import paramiko
from datetime import datetime

ERROR_LOG = 'errors.log'
HKEY = 'YOUR_RSA.key' #RSA host key

global ATTEMPTS
ATTEMPTS = 'attempts.dat' #File path to the login attempts list
PORT = 22
logging.basicConfig(filename=ERROR_LOG)
logger = logging.getLogger()
host_key = paramiko.RSAKey(filename=HKEY)


class Server(paramiko.ServerInterface):
    def __init__(self, ip):
        self.event = threading.Event()
        self.ip = ip
    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED

    def check_auth_password(self, username, password):
        #Log the password and username: (date/time | IP | user | pw) ; separator: spacebar
        if((username + password).isalnum() == True):
            attempt= datetime.now().strftime('%Y-%m-%d %H:%M:%S') + " " + self.ip + " " + username + " " + password + '\n'
            mylog = open(ATTEMPTS, 'a')
            mylog.write(attempt)
            mylog.close()
        #Always mark the login attempt as failed
        return paramiko.AUTH_FAILED

    #Allow password authentication only.
    def get_allowed_auths(self, username):
        return 'password'
        
#Setup server to listen on designed port.
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('', PORT))
sock.listen(100)
while True:

    try:
        client, addr = sock.accept()
        t = paramiko.Transport(client)
        t.add_server_key(host_key)
        server = Server(ip = str(addr[0]))
        t.start_server(server=server)
        # 5 second timeout for each client socket
        server.event.wait(5)
        t.close()
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as exc:
        logger.error(exc)
        t.close()
