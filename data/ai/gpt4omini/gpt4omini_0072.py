import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O', 'V', 'H', 'M']  # Up to 5 players

# Initialize board
def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

# Print the board
def print_board(board):
    os.system('clear')  # Clear the screen
    print("  " + "   ".join(chr(65 + col) for col in range(COLS)))  # Column labels A to G
    print("+" + "---+" * COLS)
    for row in range(ROWS):
        print("| " + " | ".join(board[row]) + " |")
        print("+" + "---+" * COLS)

# Validate user input
def get_valid_column(player):
    while True:
        column_input = input(f"Player {player}, please enter a column (A-G): ").upper()
        if len(column_input) != 1 or not column_input.isalpha():
            print("Invalid input! Please enter a single letter (A-G).")
            continue
        col_index = ord(column_input) - 65
        if 0 <= col_index < COLS:
            return col_index
        else:
            print("Column out of bounds! Please enter a letter (A-G).")

# Place a checker in the board
def place_checker(board, column, checker):
    for row in reversed(range(ROWS)):
        if board[row][column] == " ":
            board[row][column] = checker
            return True
    return False  # Column is full

# Check for a win
def check_win(board, checker):
    # Check horizontal, vertical, and diagonal
    for row in range(ROWS):
        for col in range(COLS):
            if col + 3 < COLS and all(board[row][col + i] == checker for i in range(4)):  # Horizontal
                return True
            if row + 3 < ROWS and all(board[row + i][col] == checker for i in range(4)):  # Vertical
                return True
            if row + 3 < ROWS and col + 3 < COLS and all(board[row + i][col + i] == checker for i in range(4)):  # Diagonal \
                return True
            if row - 3 >= 0 and col + 3 < COLS and all(board[row - i][col + i] == checker for i in range(4)):  # Diagonal /
                return True
    return False

# Check for a draw
def check_draw(board):
    return all(board[0][col] != " " for col in range(COLS))

# Main game loop
def play_game():
    board = create_board()
    current_player_index = random.randint(0, len(PLAYERS) - 1)
    turn_count = 0

    while True:
        print_board(board)
        current_player = PLAYERS[current_player_index]
        column = get_valid_column(current_player)

        if not place_checker(board, column, current_player):
            print("Column is full! You lose your turn.")
            current_player_index = (current_player_index + 1) % len(PLAYERS)
            continue

        turn_count += 1

        if check_win(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break
        if check_draw(board):
            print_board(board)
            print("It's a draw!")
            break

        current_player_index = (current_player_index + 1) % len(PLAYERS)

if __name__ == "__main__":
    play_game()
