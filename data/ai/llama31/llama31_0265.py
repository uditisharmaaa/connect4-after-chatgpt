import os
import random

# Constants
BOARD_WIDTH = 7
BOARD_HEIGHT = 6
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board(width, height):
    return [[" " for _ in range(width)] for _ in range(height)]

def print_board(board):
    print("  A   B   C   D   E   F   G")
    for row in board:
        print("+---+---+---+---+---+---+---+")
        print("| " + " | ".join(row) + " |")
    print("+---+---+---+---+---+---+---+")

def is_valid_input(input_char):
    return input_char.isalpha() and input_char.upper() in "ABCDEFG"

def is_valid_move(board, col):
    return board[0][col] == " "

def get_player_checker(player):
    return CHECKERS[player - 1]

def make_move(board, player, col):
    for row in reversed(board):
        if row[col] == " ":
            row[col] = get_player_checker(player)
            break

def check_win(board, player):
    checker = get_player_checker(player)
    # Check horizontal
    for row in board:
        for i in range(len(row) - 3):
            if row[i] == checker and row[i + 1] == checker and row[i + 2] == checker and row[i + 3] == checker:
                return True
    # Check vertical
    for col in range(len(board[0])):
        for i in range(len(board) - 3):
            if board[i][col] == checker and board[i + 1][col] == checker and board[i + 2][col] == checker and board[i + 3][col] == checker:
                return True
    # Check diagonal (top-left to bottom-right)
    for row in range(len(board) - 3):
        for col in range(len(board[0]) - 3):
            if board[row][col] == checker and board[row + 1][col + 1] == checker and board[row + 2][col + 2] == checker and board[row + 3][col + 3] == checker:
                return True
    # Check diagonal (bottom-left to top-right)
    for row in range(3, len(board)):
        for col in range(len(board[0]) - 3):
            if board[row][col] == checker and board[row - 1][col + 1] == checker and board[row - 2][col + 2] == checker and board[row - 3][col + 3] == checker:
                return True
    return False

def check_draw(board):
    return all([cell!= " " for row in board for cell in row])

def main():
    board = create_board(BOARD_WIDTH, BOARD_HEIGHT)
    players = list(range(1, NUM_PLAYERS + 1))
    random.shuffle(players)
    current_player = 0
    while True:
        os.system('clear')
        print_board(board)
        print(f"Player {get_player_checker(players[current_player])}, please enter a column:")
        input_char = input().upper()
        if not is_valid_input(input_char):
            print("Invalid input. Please enter a letter from A to G.")
            continue
        col = ord(input_char) - ord('A')
        if not is_valid_move(board, col):
            print("Invalid move. Column is full.")
            continue
        make_move(board, players[current_player], col)
        if check_win(board, players[current_player]):
            os.system('clear')
            print_board(board)
            print(f"Player {get_player_checker(players[current_player])} won!")
            break
        if check_draw(board):
            os.system('clear')
            print_board(board)
            print("It's a draw!")
            break
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
