import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"][:PLAYERS]
COLUMN_LABELS = [chr(i) for i in range(65, 65 + COLUMNS)]

# Function to create an empty board
def create_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

# Function to print the board
def print_board(board):
    os.system('clear')  # Clear the screen (works on Linux/Unix)
    print("  " + "   ".join(COLUMN_LABELS))
    print("+---" * COLUMNS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

# Function to get the lowest available row in a column
def get_available_row(board, column):
    for row in range(ROWS - 1, -1, -1):
        if board[row][column] == " ":
            return row
    return None

# Function to check if a move is valid
def is_valid_move(board, column):
    return 0 <= column < COLUMNS and board[0][column] == " "

# Function to place a checker
def place_checker(board, column, checker):
    row = get_available_row(board, column)
    if row is not None:
        board[row][column] = checker
        return True
    return False

# Function to check for a win
def check_win(board, checker):
    # Check horizontal, vertical, and diagonal directions
    for row in range(ROWS):
        for col in range(COLUMNS):
            if (
                # Horizontal
                col + 3 < COLUMNS and
                all(board[row][col + i] == checker for i in range(4))
                or
                # Vertical
                row + 3 < ROWS and
                all(board[row + i][col] == checker for i in range(4))
                or
                # Diagonal (\)
                row + 3 < ROWS and col + 3 < COLUMNS and
                all(board[row + i][col + i] == checker for i in range(4))
                or
                # Diagonal (/)
                row + 3 < ROWS and col - 3 >= 0 and
                all(board[row + i][col - i] == checker for i in range(4))
            ):
                return True
    return False

# Function to check if the board is full
def is_draw(board):
    return all(board[0][col] != " " for col in range(COLUMNS))

# Main function to play the game
def play_game():
    board = create_board()
    current_player = random.randint(0, PLAYERS - 1)  # Randomly select the first player
    print_board(board)

    while True:
        print(f"Player {CHECKERS[current_player]}, please enter a column:")
        move = input().strip().upper()

        if len(move) != 1 or move not in COLUMN_LABELS:
            print("Invalid input. Please enter a valid column letter.")
            continue

        column = COLUMN_LABELS.index(move)

        if not is_valid_move(board, column):
            print("Column is full or invalid. Please try another column.")
            continue

        # Place the checker and check for win/draw
        place_checker(board, column, CHECKERS[current_player])
        print_board(board)

        if check_win(board, CHECKERS[current_player]):
            print(f"Player {CHECKERS[current_player]} won!")
            break

        if is_draw(board):
            print("It's a draw!")
            break

        # Switch turn to the next player
        current_player = (current_player + 1) % PLAYERS

# Start the game
if __name__ == "__main__":
    play_game()
