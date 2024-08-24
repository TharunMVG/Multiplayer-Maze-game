import socket
import pickle
import ssl

class Network:
    def __init__(self):
        
        self.server = "localhost"
        self.port = 6000
        self.server_sni_hostname = 'example.com'
        self.server_cert = 'server.crt'
        self.client_cert = 'client.crt'
        self.client_key = 'client.key'   
        self.context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=self.server_cert) 
        self.context.load_cert_chain(certfile=self.client_cert, keyfile=self.client_key)  
        self.context.check_hostname = False
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn=self.context.wrap_socket(self.client, server_side=False, server_hostname=self.server_sni_hostname)
        self.addr = (self.server, self.port)
        self.p = None  # Initialize to None until connected
    
    def connect(self):
        try:
            self.conn.connect(self.addr)
            self.p = self.receive_data()
            return self.p
        except socket.error as e:
            print("Error connecting to server:", e)
            return None
    
    def getP(self):
        return self.p

    def send(self, data):
        try:
            self.conn.send(pickle.dumps(data))
            return self.receive_data()
        except socket.error as e:
            print("Error sending data:", e)
            return None
    
    def receive_data(self):
        try:
            return pickle.loads(self.conn.recv(2048))
        except socket.error as e:
            print("Error receiving data:", e)
            return None
