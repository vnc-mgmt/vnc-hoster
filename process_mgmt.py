import subprocess

class VNCServer:
    def __init__(self, debug, port, user=None):
        self.debug = debug
        self.port = port
        self.user = user
        self.server_process = None
        self.novnc_process = None
    def start_server_process(self):
        if self.debug:
            print('start_server_process called, port {}'.format(self.port))
        else:
            self.server_process = subprocess.Popen(['vncserver', '-rfbport', str(self.port-1)])
    def start_novnc_process(self):
        if self.debug:
            print('start_novnc_process called, port {}'.format(self.port))
        else:
            self.novnc_process = subprocess.Popen(['./novnc/utils/novnc_proxy', '--listen', str(self.port), '--vnc', str(self.port-1)])
    def start(self):
        self.start_novnc_process()
        self.start_server_process()
