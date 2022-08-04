from flask import Flask, request
import requests
import process_mgmt
import os
import crypt
import pwd

app = Flask(__name__)

vnc_servers = {}

def auth(auth):
    r = requests.post('http://{}:4583/auth'.format(app.server_ip), data={'auth': auth})
    authenticated = None
    if r.text == 'False':
        authenticated = False
    else:
        authenticated = int(r.text)
    return authenticated

def get_vnc_data():
    r = requests.get('http://{}:4583/vnc_data'.format(app.server_ip))
    return r.json()

def create_vncserver(user, passwd, sudo):
    found = False
    for p in pwd.getpwall():
        if p.pw_name == user:
            found = True
    if not found:
        os.system('useradd -m {}'.format(user))
        hashed_passwd = crypt.crypt(passwd)
        os.system("echo '{}:{}' | chpasswd -e".format(user, hashed_passwd))
        if sudo:
            os.system('usermod -aG sudo {}'.format(user))

def start_vncserver(port):
    vnc_servers[port] = process_mgmt.VNCServer(app.debug_mode, port)
    vnc_servers[port].start()
    return 'done'

def stop_vncserver(port):
    try:
        vnc_servers[port].terminate()
    except:
        return 'vnc already stopped'
    return 'done'

@app.route('/create', methods=['POST'])
def create_vnc():
    if not app.debug_mode:
        data = dict(request.form)
        auth_details = data['auth']
        port = int(data['port'])
        authenticated = auth(auth_details)
        if not authenticated == False:
            sudo = authenticated >= 2
            create_vncserver(auth_details.split(':')[0], auth_details.split(':')[1], sudo)
    else:
        data = dict(request.form)
        port = int(data['port'])
        print('create_vnc() called for port {}'.format(port))
    return 'done'

@app.route('/start', methods=['POST'])
def start_vnc():
    data = dict(request.form)
    auth_details = data['auth']
    port = int(data['port'])
    authenticated = auth(auth_details)
    if not authenticated == False:
        permissions = authenticated
        vnc_data = get_vnc_data()
        if str(port) in vnc_data:
            if permissions == 0:
                if auth_details.split(':')[0] == vnc_data[str(port)]['username']:
                    start_vncserver(port)
                else:
                    return 'unprivileged', 401
            else:
                return start_vncserver(port)
        else:
            return 'vnc notfound', 404

@app.route('/ping')
def ping():
    return 'pong'

@app.route('/stop', methods=['POST'])
def stop_vnc():
    data = dict(request.form)
    auth_details = data['auth']
    port = int(data['port'])
    authenticated = auth(auth_details)
    if not authenticated == False:
        permissions = authenticated
        vnc_data = get_vnc_data()
        if str(port) in vnc_data:
            if permissions == 0:
                if auth_details.split(':')[0] == vnc_data[str(port)]['username']:
                    stop_vncserver(port)
                else:
                    return 'unprivileged', 401
            else:
                return stop_vncserver(port)
        else:
            return 'vnc notfound', 404

def run_server(server_ip, debug):
    app.server_ip = server_ip
    app.debug_mode = debug
    app.run(host='0.0.0.0', port=4584)
