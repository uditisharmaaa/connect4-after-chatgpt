import os
import random

COLUMNS = 7
ROWS = 6
MAX_PLAYERS = 5
PLAYERS = ["X", "O", "V", "H", "M"]
NUM_PLAYERS = 2

def create_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    print("  " + "   ".join(chr(65 + i) for i in range(COLUMNS)))
    for row in board:
        print("+---" * COLUMNS + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * COLUMNS + "+")

def get_move(current_player):
    while True:
        move = input(f"Player {current_player}, please enter a column: ").strip().upper()
        if len(move) == 1 and 'A' <= move <= 'G':
            return ord(move) - ord('A')
        print("Invalid input. Try again.")

def apply_move(board, column, player):
    for row in range(ROWS-1, -1, -1):
        if board[row][column] == " ":
            board[row][column] = player
            return True
    return False

def check_win(board, player):
    # Check horizontal
    for r in range(ROWS):
        for c in range(COLUMNS-3):
            if all(board[r][c+i] == player for i in range(4)):
                return True

    # Check vertical
    for c in range(COLUMNS):
        for r in range(ROWS-3):
            if all(board[r+i][c] == player for i in range(4)):
                return True

    # Check diagonal /
    for r in range(3, ROWS):
        for c in range(COLUMNS-3):
            if all(board[r-i][c+i] == player for i in range(4)):
                return True

    # Check diagonal \
    for r in range(ROWS-3):
        for c in range(COLUMNS-3):
            if all(board[r+i][c+i] == player for i in range(4)):
                return True

    return False

def check_draw(board):
    return all(board[0][c] != " " for c in range(COLUMNS))

def play_game():
    board = create_board()
    current_player_index = random.randint(0, NUM_PLAYERS-1)
    current_player = PLAYERS[current_player_index]
    print_board(board)

    while True:
        move = get_move(current_player)
        if apply_move(board, move, current_player):
            print_board(board)
            if check_win(board, current_player):
                print(f"Player {current_player} won!")
                break
            elif check_draw(board):
                print("The game is a draw!")
                break
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            current_player = PLAYERS[current_player_index]
        else:
            print("Column full. Turn lost.")

play_game()
