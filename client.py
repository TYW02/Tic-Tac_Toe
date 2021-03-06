import socket
import threading


class TicTacToe:

    def __init__(self):
        self.board = [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]]
        # X starts the turn, X is also the one who hosts the game
        self.turn = "X"
        self.you = "X"
        self.opponent = "O"
        self.winner = None
        self.game_over = False

        # Turn counter if counter is 9 it means it is a draw
        self.counter = 0

    def host_game(self, host, port):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((host, port))
        # Listening for 1 connection
        server.listen(1)

        client, addr = server.accept()

        self.you = "X"
        self.opponent = "O"
        threading.Thread(target=self.handle_connection, args=(client,)).start()
        # Close server here we don't need to wait for more connections when we already have one
        server.close()

    def connect_to_game(self, host, port):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((host, port))

        self.you = 'O'
        self.opponent = 'X'
        threading.Thread(target=self.handle_connection, args=(client,)).start()

    def handle_connection(self, client):
        while not self.game_over:
            # If its your turn...
            if self.turn == self.you:
                move = input("Enter Your Move (Row,Col): ")
                if self.check_valid_move(move.split(',')):
                    client.send(move.encode('utf-8'))
                    # Apply the move with your symbol, then change turn
                    self.apply_move(move.split(','), self.you)
                    self.turn = self.opponent

                else:
                    print("Invalid Move")
            else:
                # 1024 bytes
                data = client.recv(1024)
                if not data:
                    break
                else:
                    self.apply_move(data.decode('utf-8').split(','), self.opponent)
                    self.turn = self.you
        client.close()

    def apply_move(self, move, player):
        if self.game_over:
            return
        self.counter += 1
        # Player is the symbol
        self.board[int(move[0])][int(move[1])] = player
        self.print_board()
        if self.check_if_won():
            if self.winner == self.you:
                print("You WON!")
                exit()
            elif self.winner == self.opponent:
                print("You LOSE!")
                exit()
        else:
            if self.counter == 9:
                print("DRAW!")
                exit()

    def check_valid_move(self, move):
        # If board at this position is empty
        return self.board[int(move[0])][int(move[1])] == " "

    def check_if_won(self):
        for row in range(3):
            # Checks for row winning condition
            # and if the symbol is not the default symbol
            if self.board[row][0] == self.board[row][1] == self.board[row][2] != " ":
                self.winner = self.board[row][0]
                self.game_over = True
                return True

        for col in range(3):
            # Checks for column winning condition
            # and if the symbol is not the default symbol
            if self.board[0][col] == self.board[1][col] == self.board[2][col] != " ":
                self.winner = self.board[0][col]
                self.game_over = True
                return True

        # Check for diagonal winning condition (from top left to bottom right)
        # and if the symbol is not the default symbol
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != " ":
            self.winner = self.board[0][0]
            self.game_over = True
            return True

        # Check for diagonal winning condition (from top right to bottom left)
        # and if the symbol is not the default symbol
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != " ":
            self.winner = self.board[0][2]
            self.game_over = True
            return True
        return False

    def print_board(self):
        for row in range(3):
            print(" | ".join(self.board[row]))
            # if row is not the last row print the separator
            if row != 2:
                print("-----------")


game = TicTacToe()
# Change localhost to IP address of host
game.connect_to_game("localhost", 9999)
