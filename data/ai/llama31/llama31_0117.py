import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    print("  A B C D E F G")
    for row in board:
        print("+---+" * COLUMNS)
        print("| {} |".format(" | ".join(row)))
    print("+---+" * COLUMNS)

def get_player_move(player):
    while True:
        move = input("Player {}, please enter a column: ".format(player)).upper()
        if move in "ABCDEFG" and ord(move) - ord('A') < COLUMNS:
            return ord(move) - ord('A')
        print("Invalid input, please try again.")

def place_checker(board, player, column):
    for row in reversed(board):
        if row[column] == " ":
            row[column] = player
            return

def check_win(board, player):
    # Check horizontal
    for row in board:
        for i in range(len(row) - 3):
            if row[i] == row[i+1] == row[i+2] == row[i+3] == player:
                return True
    # Check vertical
    for col in range(len(board[0])):
        for i in range(len(board) - 3):
            if board[i][col] == board[i+1][col] == board[i+2][col] == board[i+3][col] == player:
                return True
    # Check diagonal (top-left to bottom-right)
    for row in range(len(board) - 3):
        for col in range(len(board[0]) - 3):
            if board[row][col] == board[row+1][col+1] == board[row+2][col+2] == board[row+3][col+3] == player:
                return True
    # Check diagonal (bottom-left to top-right)
    for row in range(3, len(board)):
        for col in range(len(board[0]) - 3):
            if board[row][col] == board[row-1][col+1] == board[row-2][col+2] == board[row-3][col+3] == player:
                return True
    return False

def check_draw(board):
    return all([all([cell!= " " for cell in row]) for row in board])

def game():
    board = create_board()
    players = CHECKERS[:PLAYERS]
    current_player = random.choice(players)
    while True:
        print_board(board)
        column = get_player_move(current_player)
        place_checker(board, current_player, column)
        if check_win(board, current_player):
            print_board(board)
            print("Player {} won!".format(current_player))
            break
        if check_draw(board):
            print_board(board)
            print("It's a draw!")
            break
        current_player = players[(players.index(current_player) + 1) % PLAYERS]

game()
