import socket
from _thread import *
import sys
import pickle
from character import *
from animation_player.animationManager import AnimationManager


server = "192.168.0.11"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")

players = [DummyCharacter(256, 256, 100, 100, 0, 100, [], States.IDLE, False), DummyCharacter(512, 512, 100, 100, 0, 100, [], States.IDLE, False)]

def player_reset(index):
    players[index] = DummyCharacter(256, 256, 100, 100, 0, 100, [], States.IDLE, False)

def threaded_client(conn, player):
    global current_player
    conn.send(pickle.dumps([players[player], players[(player + 1) % 2]]))
    reply = ""
    while True:
        try:
           # data = pickle.loads(conn.recv(2048))
           # if type(data) == Character:
           #     players[player] = data
#
           #     if not data:
           #         print("Disconnected")
           #         break
           #     else:
            conn.sendall(pickle.dumps([players[player].hp, players[player].absorb_shield, players[player].speed]))
            data = pickle.loads(conn.recv(2048))
            players[player] = data

            reply = players[(player + 1) % 2]
                #print(f'Received: {data}')
                #print(f'Sending: {reply}')
            conn.sendall(pickle.dumps(reply))

            data = pickle.loads(conn.recv(2048))

            if type(data) == list:
                #print(data)
                players[(player + 1) % 2].hp = data[0]
                players[(player + 1) % 2].speed = data[1]
                players[(player + 1) % 2].absorb_shield += data[2]


            players[player].absorb_shield += pickle.loads(conn.recv(2048))


        except:
            break

    print("Lost connection")
    conn.close()

    current_player = player
    player_reset(player)


current_player = 0
while True:
    conn, addr = s.accept()
    print(f'Connected to: {addr}')

    start_new_thread(threaded_client, (conn, current_player))
    current_player += 1
