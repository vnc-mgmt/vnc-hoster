from flask import Flask, request
import requests
import process_mgmt

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

def start_vncserver(port):
    vnc_servers[port] = process_mgmt.VNCServer(app.debug_mode, port)
    vnc_servers[port].start()
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
        if port in vnc_data:
            if permissions == 0:
                if auth_details.split(':')[0] == vnc_data[port]['username']:
                    start_vncserver(port)
                else:
                    return 'unprivileged'
            else:
                return start_vncserver(port)
        else:
            return 'vnc notfound'

def run_server(server_ip, debug):
    app.server_ip = server_ip
    app.debug_mode = debug
    app.run(host='0.0.0.0', port=4584)
