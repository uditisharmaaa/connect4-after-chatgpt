import os
import random

# Constants for game settings
ROWS = 6
COLS = 7
MAX_PLAYERS = 5
PLAYERS = ["X", "O", "V", "H", "M"]

# Create an empty game board
def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

# Print the game board
def print_board(board):
    os.system('clear')  # Clear the console for a clean view
    print("  " + "   ".join(chr(i) for i in range(65, 65 + COLS)))  # Column labels A-G
    print("+" + "---+" * COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)

# Check if a position is valid for placing a checker
def is_valid_column(board, column):
    return 0 <= column < COLS and board[0][column] == " "

# Place a checker in the specified column
def place_checker(board, column, checker):
    for row in reversed(board):
        if row[column] == " ":
            row[column] = checker
            return

# Check for a win condition
def check_win(board, checker):
    # Check horizontal, vertical, and diagonal win conditions
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == checker:
                # Horizontal
                if col + 3 < COLS and all(board[row][col + i] == checker for i in range(4)):
                    return True
                # Vertical
                if row + 3 < ROWS and all(board[row + i][col] == checker for i in range(4)):
                    return True
                # Diagonal /
                if row + 3 < ROWS and col - 3 >= 0 and all(board[row + i][col - i] == checker for i in range(4)):
                    return True
                # Diagonal \
                if row + 3 < ROWS and col + 3 < COLS and all(board[row + i][col + i] == checker for i in range(4)):
                    return True
    return False

# Check for a draw condition
def check_draw(board):
    return all(board[0][col] != " " for col in range(COLS))

# Main game loop
def main():
    board = create_board()
    current_player_index = random.randint(0, 1)  # Randomly choose the starting player
    player_count = 2

    print_board(board)

    while True:
        current_checker = PLAYERS[current_player_index % player_count]
        column_input = input(f"Player {current_checker}, please enter a column (A-G): ").upper()

        if len(column_input) != 1 or not column_input.isalpha():
            print("Invalid input. Please enter a valid column letter.")
            continue

        column = ord(column_input) - 65  # Convert letter A-G to column index (0-6)

        if not is_valid_column(board, column):
            print("Column is full or invalid. Please choose another column.")
            continue

        place_checker(board, column, current_checker)
        print_board(board)

        if check_win(board, current_checker):
            print(f"Player {current_checker} won!")
            break

        if check_draw(board):
            print("The game is a draw!")
            break

        current_player_index += 1  # Switch to the next player

if __name__ == "__main__":
    main()
