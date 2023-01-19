from bcolors import BColors as bc
import socket
from _thread import start_new_thread
import pickle
# from new_client_thread import threaded_client
from game import Game

# Server's address
server = ""
port = 5555

# Assigning socket and verifying if the connection can be made, if not, return an error
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# server_ip = socket.gethostbyname(server)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

# Trying to listen, if successful, server running fine
s.listen()
print(bc.HEADER + "Server started!" + bc.END)
print(bc.WARNING + "Waiting for a connection..." + bc.END)

connected = set()
games = {}
id_count = 0


def threaded_client(conn, current_player, games, game_id):
    global id_count
    conn.send(str.encode(str(current_player)))

    reply = ""

    while True:

        try:
            data = conn.recv(4096).decode()

            if game_id in games:
                game = games[game_id]

                if not data:
                    break
                else:
                    if data == "reset":
                        game.reset_went()
                    elif data != "get":
                        game.play(current_player, data)

                    reply = game
                    conn.sendall(pickle.dumps(reply))

            else:
                break
        except:
            break

    print(bc.FAIL + "LOST CONNECTION" + bc.END)

    try:
        del games[game_id]
        print(bc.WARNING + f"Closing game {game_id}" + bc.END)
    except:
        pass

    id_count -= 1
    conn.close()


while True:
    conn, addr = s.accept()
    print(bc.GREEN + f"Connected to: {addr}" + bc.END)

    id_count += 1
    p = 0
    game_id = (id_count - 1) // 2
    if id_count % 2 == 1:
        games[game_id] = Game(game_id)
        print("Creating a new game...")
    else:
        games[game_id].ready = True
        p = 1

    start_new_thread(threaded_client, (conn, p, games, game_id))
