import os
import random

# Constants
ROWS = 6
COLS = 7
MAX_PLAYERS = 5
CHECKERS = ["X", "O", "V", "H", "M"]

def print_board(board):
    os.system('clear')
    print("  " + "   ".join(chr(ord('A') + i) for i in range(COLS)))
    print("+---" * COLS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLS + "+")

def init_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def valid_input(player_input):
    return len(player_input) == 1 and 'A' <= player_input <= chr(ord('A') + COLS - 1)

def place_checker(board, column, checker):
    col_index = ord(column) - ord('A')
    for row in reversed(board):
        if row[col_index] == " ":
            row[col_index] = checker
            return True
    return False

def check_winner(board, checker):
    # Check horizontal, vertical and diagonal wins
    for row in range(ROWS):
        for col in range(COLS):
            if col <= COLS - 4 and all(board[row][col+i] == checker for i in range(4)):
                return True
            if row <= ROWS - 4 and all(board[row+i][col] == checker for i in range(4)):
                return True
            if row <= ROWS - 4 and col <= COLS - 4 and all(board[row+i][col+i] == checker for i in range(4)):
                return True
            if row >= 3 and col <= COLS - 4 and all(board[row-i][col+i] == checker for i in range(4)):
                return True
    return False

def check_draw(board):
    return all(cell != " " for row in board for cell in row)

def play_game(players_count):
    board = init_board()
    current_player = random.choice(range(players_count))
    print_board(board)

    while True:
        player_checker = CHECKERS[current_player]
        player_input = input(f"Player {player_checker}, please enter a column: ").strip()

        while not valid_input(player_input):
            print("Invalid input, try again.")
            player_input = input(f"Player {player_checker}, please enter a column: ").strip()

        if not place_checker(board, player_input, player_checker):
            print("Column full, turn lost.")
            current_player = (current_player + 1) % players_count
            continue

        print_board(board)
        
        if check_winner(board, player_checker):
            print(f"Player {player_checker} won!")
            break

        if check_draw(board):
            print("The game is a draw!")
            break

        current_player = (current_player + 1) % players_count

if __name__ == "__main__":
    play_game(players_count=2)
