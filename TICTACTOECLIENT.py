import socket

# Create a socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 6234))

# Determines what player you are
player = client_socket.recv(2048).decode()
print(f"You are {player}")

while True:
    #First check to see if we have a win before we ask for input
    data = client_socket.recv(2048).decode()
    if "wins!" in data or "It's a tie!" in data:
        print(data)
        break
#Only accept input if it is your turn
    if data == "Your turn":
        move = input("Enter your move (row, col): ")
        client_socket.send(move.encode())
    else:
        print(data)

client_socket.close()