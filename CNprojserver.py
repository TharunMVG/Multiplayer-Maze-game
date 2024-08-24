import socket
from _thread import *
from player import Player
import pickle
import ssl

server = "localhost"
port = 6000
server_cert = 'server.crt'
server_key = 'server.key'
client_certs = 'client.crt'

context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.verify_mode = ssl.CERT_REQUIRED
context.load_cert_chain(certfile=server_cert, keyfile=server_key)
context.load_verify_locations(cafile=client_certs)

maze = [
    "##########",
    "#        #",
    "#  ##### #",
    "#  #     #",
    "#  #     #",
    "#  #     #",
    "#  #     #",
    "#     #  #",
    "#     #  #",
    "##########"
]
s = socket.socket()

treasure_pos = (300,300)
try:
    s.bind((server, port))
except socket.error as e:
    print(str(e))

s.listen(2)
print("Waiting for a connection, Server Started")

players = [Player(65, 65, 30, 30, (255, 0, 0),maze), Player(200, 200, 30, 30, (0, 0, 255),maze)]

def threaded_client(conn, player):
    conn.send(pickle.dumps(players[player]))
    reply = ""
    while True:
        try:
            data = pickle.loads(conn.recv(2048))
            players[player] = data

            if not data:
                print("Disconnected")
                break
            else:
                if player == 1:
                    reply = players[0]
                else:
                    reply = players[1]
                
            conn.sendall(pickle.dumps(reply))
        except:
            break
    print("Lost Connection")
    conn.close()

currentPlayer = 0

while True:
    newsocket, addr = s.accept()
    print("Connected to: ", addr)
    conn = context.wrap_socket(newsocket, server_side=True)
    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1
