import os
import random

# Constants for board dimensions and players
ROWS = 6
COLS = 7
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]
NUM_PLAYERS = 2

def initialize_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    os.system('clear')
    # Print column headers
    header = "  " + "   ".join(chr(65 + i) for i in range(COLS))
    print(header)
    # Print the board
    for row in board:
        print("+---" * COLS + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * COLS + "+")

def check_for_win(board, player):
    # Check horizontal win
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col + i] == player for i in range(4)):
                return True

    # Check vertical win
    for col in range(COLS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == player for i in range(4)):
                return True

    # Check diagonal (top-left to bottom-right) win
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == player for i in range(4)):
                return True

    # Check diagonal (bottom-left to top-right) win
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i][col + i] == player for i in range(4)):
                return True

    return False

def check_for_draw(board):
    return all(board[0][col] != " " for col in range(COLS))

def get_valid_column():
    while True:
        choice = input("Please enter a column (A-G): ").upper()
        if len(choice) == 1 and 'A' <= choice <= chr(65 + COLS - 1):
            return ord(choice) - 65
        print("Invalid input. Please enter a valid column letter.")

def play_game():
    board = initialize_board(ROWS, COLS)
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)
    player_symbols = PLAYER_SYMBOLS[:NUM_PLAYERS]

    print_board(board)

    while True:
        current_player = player_symbols[current_player_idx]
        print(f"Player {current_player}, it is your turn.")
        col = get_valid_column()

        # Find the first available row from the bottom
        for row in range(ROWS - 1, -1, -1):
            if board[row][col] == " ":
                board[row][col] = current_player
                break
        else:
            print("Column full! You lose your turn.")
            continue

        print_board(board)

        if check_for_win(board, current_player):
            print(f"Player {current_player} won!")
            break
        elif check_for_draw(board):
            print("The game is a draw!")
            break

        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    play_game()
