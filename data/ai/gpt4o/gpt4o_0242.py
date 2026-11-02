import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]  # Up to 5 players
NUM_PLAYERS = 2  # Set to 2 for the assignment requirement

# Create the board
def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

# Print the board
def print_board(board):
    os.system('clear')  # Clear the console
    # Print column headers
    headers = '  '.join(chr(ord('A') + i) for i in range(COLS))
    print("  " + headers)
    # Print board
    for row in board:
        print("+---" * COLS + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * COLS + "+")

# Check for a win
def check_win(board, symbol):
    # Horizontal check
    for r in range(ROWS):
        for c in range(COLS - 3):
            if all(board[r][c + i] == symbol for i in range(4)):
                return True

    # Vertical check
    for r in range(ROWS - 3):
        for c in range(COLS):
            if all(board[r + i][c] == symbol for i in range(4)):
                return True

    # Diagonal (\) check
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if all(board[r + i][c + i] == symbol for i in range(4)):
                return True

    # Diagonal (/) check
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if all(board[r - i][c + i] == symbol for i in range(4)):
                return True

    return False

# Check for a draw
def check_draw(board):
    return all(all(cell != " " for cell in row) for row in board)

# Place a checker
def place_checker(board, col, symbol):
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = symbol
            return True
    return False  # Column is full

# Main game loop
def connect_four():
    board = create_board()
    current_players = PLAYER_SYMBOLS[:NUM_PLAYERS]
    current_player = random.choice(current_players)  # Randomly choose the first player
    print_board(board)

    while True:
        print(f"Player {current_player}, please enter a column:")
        col_input = input().strip().upper()

        if col_input not in {chr(x) for x in range(ord('A'), ord('A') + COLS)}:
            print("Invalid input. Please enter a valid column letter (A-G).")
            continue

        col = ord(col_input) - ord('A')

        if place_checker(board, col, current_player):
            print_board(board)

            if check_win(board, current_player):
                print(f"Player {current_player} won!")
                break

            if check_draw(board):
                print("The game is a draw!")
                break

            # Alternating players
            current_player_index = current_players.index(current_player)
            current_player = current_players[(current_player_index + 1) % NUM_PLAYERS]
        else:
            print("Column is full. Try another column.")

# Run the game
if __name__ == "__main__":
    connect_four()
