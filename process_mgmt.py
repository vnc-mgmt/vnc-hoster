import subprocess

class VNCServer:
    def __init__(self, debug, port, user):
        self.debug = debug
        self.port = port
        self.user = user
        self.server_process = None
        self.novnc_process = None
    def start_server_process(self):
        if self.debug:
            print('start_server_process called, port {}'.format(self.port-1))
        else:
            self.server_process = subprocess.Popen(['runuser', '-l', self.user, '-c', 'vncserver :{}'.format(str(self.port-1))])
    def start_novnc_process(self):
        if self.debug:
            print('start_novnc_process called, port {}'.format(self.port))
        else:
            self.novnc_process = subprocess.Popen(['./novnc/utils/novnc_proxy', '--listen', str(self.port), '--vnc', 'localhost:' + str(self.port-1)])
    def terminate_server_process(self):
        if self.debug:
            print('terminate_server_process called, port {}'.format(self.port-1))
        else:
            self.server_process.terminate()
    def terminate_novnc_process(self):
        if self.debug:
            print('terminate_novnc_process called, port {}'.format(self.port))
        else:
            self.novnc_process.terminate()
    def start(self):
        self.start_novnc_process()
        self.start_server_process()
    def terminate(self):
        self.terminate_novnc_process()
        self.terminate_server_process()
