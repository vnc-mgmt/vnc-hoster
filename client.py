import requests
import api_endpoint
import socket
import os
import sys

if not os.path.exists('server_ip.conf'):
    open('server_ip.conf', 'x').close()
    print('Server IP Not set')
else:
    server_ip_f = open('server_ip.conf')
    server_ip = server_ip_f.read().replace('\n', '')
    server_ip_f.close()
    hostname = socket.gethostname()

if os.path.exists('debug'):
    debug = True
else:
    debug = False

if not os.path.exists('novnc') and not debug:
    print('noVNC does not exist, run this to clone it:')
    print('git clone https://github.com/novnc/novnc')
    sys.exit(1)

r = requests.get('http://{}:4583/add/{}'.format(server_ip, hostname))

api_endpoint.run_server(server_ip, debug)
