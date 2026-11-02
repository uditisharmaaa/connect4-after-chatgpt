import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = ["X", "O"]  # up to 5 players can be used by assigning more letters

# Function to create the board
def create_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

# Function to print the board
def print_board(board):
    os.system('clear')  # Clear the terminal screen
    print("  " + "   ".join(chr(65 + i) for i in range(COLUMNS)))  # Column labels A, B, C, ...
    print("+" + "---+" * COLUMNS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLUMNS)

# Function to drop the checker
def drop_checker(board, col, player):
    for row in reversed(board):
        if row[col] == " ":
            row[col] = player
            return True
    return False

# Function to validate input
def is_valid_input(col):
    return col.isalpha() and len(col) == 1 and 'A' <= col.upper() <= chr(65 + COLUMNS - 1)

# Function to check for a win
def check_winner(board, player):
    # Check horizontal
    for row in board:
        for c in range(COLUMNS - 3):
            if all(cell == player for cell in row[c:c + 4]):
                return True

    # Check vertical
    for c in range(COLUMNS):
        for r in range(ROWS - 3):
            if all(board[r + i][c] == player for i in range(4)):
                return True

    # Check diagonal (top-left to bottom-right)
    for r in range(ROWS - 3):
        for c in range(COLUMNS - 3):
            if all(board[r + i][c + i] == player for i in range(4)):
                return True

    # Check diagonal (bottom-left to top-right)
    for r in range(3, ROWS):
        for c in range(COLUMNS - 3):
            if all(board[r - i][c + i] == player for i in range(4)):
                return True

    return False

# Function to check for a draw
def check_draw(board):
    return all(cell != " " for row in board for cell in row)

# Main game function
def play_game():
    board = create_board()
    current_player_index = random.randint(0, len(PLAYERS) - 1)

    while True:
        print_board(board)
        current_player = PLAYERS[current_player_index]
        col = input(f"Player {current_player}, please enter a column: ").upper()

        if is_valid_input(col):
            col_index = ord(col) - 65  # Convert letter A-G to index 0-6
            if drop_checker(board, col_index, current_player):
                if check_winner(board, current_player):
                    print_board(board)
                    print(f"Player {current_player} won!")
                    break
                if check_draw(board):
                    print_board(board)
                    print("The game is a draw!")
                    break
                current_player_index = (current_player_index + 1) % len(PLAYERS)
            else:
                print("The column is full. Try again.")
        else:
            print("Invalid input. Please enter a valid column (A-G).")

# Entry point of the program
if __name__ == "__main__":
    play_game()
