import socket as s
import json
import sys
import ssl


def main():
    # default TCP port
    port = 27993
    use_tcp = True

    # check if there are enough command-line arguments
    if len(sys.argv) < 3:
        usage()
    # handle the case when a specific port is specified
    elif sys.argv[1] == '-p':
        port = int(sys.argv[2])

        # check whether the is TLS
        if sys.argv[3] == '-s':
            hostname = sys.argv[4]
            username = sys.argv[5]
            return client(port, not use_tcp, hostname, username)
        hostname = sys.argv[3]
        username = sys.argv[4]
        return client(port, use_tcp, hostname, username)

    # handle the case where no specific port is specified
    elif sys.argv[1] == '-s':
        port = 27994
        hostname = sys.argv[2]
        username = sys.argv[3]
        return client(port, not use_tcp, hostname, username)
    hostname = sys.argv[1]
    username = sys.argv[2]
    return client(port, use_tcp, hostname, username)


def usage():
    # make sure the command line input follows the syntax exactly
    sys.stdout = sys.stderr
    print('Must follow format: $ ./client <-p port> <-s> <hostname> <Northeastern-username>')
    sys.exit(2)


def send_message(socket, message):
    # send a JSON message with \n terminator
    json_data = json.dumps(message) + "\n"
    socket.sendall(json_data.encode('utf-8'))


def receive_message(socket):
    # create a buffer to read the receiving data
    buf = ""
    while not buf.endswith("\n"):
        data = socket.recv(1024).decode('utf-8')
        buf += data
    return json.loads(buf.strip())


def client(port, use_tcp, hostname, username):
    # create a client socket object using IPv4 and TCP
    client_socket = s.socket(s.AF_INET, s.SOCK_STREAM)

    # encrypt the socket if using TLS
    if not use_tcp:
        context = ssl.create_default_context()
        client_socket = context.wrap_socket(client_socket, server_hostname=hostname)

    # connect to the server
    client_socket.connect((hostname, port))

    # prepare the hello message to start the game
    hello_message = {
        "type": "hello",
        "northeastern_username": username
    }

    send_message(client_socket, hello_message)

    # wait for a response
    response = receive_message(client_socket)

    if response.get("type") == "start":
        # save the game id for each guess
        game_id = response.get("id")

        # save all word list strings in array
        text_file = open("project1-words.txt", "r")
        word_list = text_file.read().split("\n")

        while True:
            # prompt the client for a guess
            guess_word = input("Make a guess: ")
            while guess_word not in word_list:
                print("Guess was not a word from the valid word list")
                guess_word = input("Guess a new word: ")

            guess_message = {
                "type": "guess",
                "id": game_id,
                "word": guess_word
            }

            send_message(client_socket, guess_message)

            # receive server response
            response = receive_message(client_socket)

            if response.get("type") == "bye":
                flag = response.get("flag")
                print(flag)
                # close the text file after game is over
                text_file.close()
                break
            elif response.get("type") == "error":
                # server detected an illegal message
                error_message = response.get("message")
                print(f"Error from server: {error_message}")
                text_file.close()
                break  # stop the program
            else:
                # only print the guesses if the user needs to make another guess
                print(response.get("guesses"))

    # close the socket connection
    client_socket.close()


main()
