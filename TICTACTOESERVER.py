import socket
import threading


board = [[' ' for _ in range(3)] for _ in range(3)]

# Create a socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 6234))
server_socket.listen(2) 

# List to store client sockets
clients = []
current_player = 'X'
players_connected = 0

# handle client connections
def handle_client(conn, player):
    global current_player
    global players_connected
    conn.send(f"Player {player}".encode())
    players_connected += 1
    game_over = False 

    while not game_over:
        #Player x/ player 1 starts the game
        if players_connected == 2 and player == current_player:
            conn.send("Your turn".encode())
            data = conn.recv(2048).decode()
            if not data:
                break
            #Split row and column input by ','
            row, col = map(int, data.split(','))
            #If this space is valid then set that space
            #Set this space = to current player value
            if 0 <= row < 3 and 0 <= col < 3 and board[row][col] == ' ':
                board[row][col] = player
                print_board()
                #Send info to both players
                broadcast(f"Player {player} moved to position ({row}, {col})\n")
                #After each move check if the we having a winning player
                if check_winner(player):
                    broadcast(f"Player {player} wins!")
                    print(f"Player {player} wins!")
                    game_over = True  
                #If we don't have any blank spaces in our board
                #Tie game
                elif ' ' not in [cell for row in board for cell in row]:
                    broadcast("Tie Game!")
                    print("Tie Game")
                    game_over = True  
                    #Update out current player after player x has made a move
                current_player = 'O' if current_player == 'X' else 'X'
            else:
                conn.send("Invalid move. Try again.".encode())

    conn.close()
    clients.remove(conn)

# Send messages to all clients
def broadcast(message):
    for client in clients:
        client.send(message.encode())


def print_board():
    for row in board:
        print(' | '.join(row))
        print('-' * 9)

# Check for a winner
def check_winner(player):
    #  rows
    for row in board:
        if row == [player] * 3:
            return True
    #  columns
    for col in range(3):
        if [board[row][col] for row in range(3)] == [player] * 3:
            return True
    # diagonals
    if [board[i][i] for i in range(3)] == [player] * 3:
        return True
    if [board[i][2 - i] for i in range(3)] == [player] * 3:
        return True
    return False

print("Server started. Waiting for two players..")

# Accept client connections
for i in range(2):
    conn, addr = server_socket.accept()
    clients.append(conn)
    #Making threads to handle players
    threading.Thread(target=handle_client, args=(conn, current_player)).start()
    current_player = 'O' if current_player == 'X' else 'X'

server_socket.close()