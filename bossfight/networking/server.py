import pickle
import socket
from _thread import *
from character import *
from states import *
import sys
import pygame

server = "localhost"
port = 12345
pygame.init()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")

players = [DummyCharacter(256, 256, 100, 100, 0, 100, [], States.IDLE, False), DummyCharacter(512, 512, 100, 100, 0, 100, [], States.IDLE, False)]

connected = [False, False]
def player_reset(index):
    players[index] = DummyCharacter(256, 256, 100, 100, 0, 100, [], States.IDLE, False)

def threaded_client(conn, player):
    global current_player
    conn.send(pickle.dumps([players[player], players[(player + 1) % 2]]))

    connected[player] = True
    while not connected[(player + 1) % 2]:
        conn.send(pickle.dumps(False))
        conn.recv(8)

    conn.send(pickle.dumps(True))
    conn.recv(8)
    while True:
        try:
            a = pickle.dumps([players[(player + 1) % 2], players[player].hp, players[player].absorb_shield, players[player].speed])
            conn.sendall(a)
            data = pickle.loads(conn.recv(2048))
            players[player] = data

                #print(f'Received: {data}')
                #print(f'Sending: {reply}')


            data = pickle.loads(conn.recv(512))


            for i in data[0]:
                players[(player + 1) % 2].deal_damage(i)
            players[(player + 1) % 2].speed = data[1]
            players[player].absorb_shield += data[2]






        except:
            break

    print("Player disconnected")
    conn.close()

    connected[player] = False
    current_player = player
    player_reset(player)


current_player = 0
while True:
    conn, addr = s.accept()
    print(f'Connected to: {addr}')

    start_new_thread(threaded_client, (conn, current_player))
    current_player += 1
