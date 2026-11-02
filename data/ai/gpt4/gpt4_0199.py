import os
import random

# Constants
ROWS = 6
COLS = 7
MAX_PLAYERS = 5
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]

# Initialize board
def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

# Print the board
def print_board(board):
    os.system('clear')
    col_labels = "   ".join(chr(65 + i) for i in range(len(board[0])))
    print(f"  {col_labels}")
    print("+" + "---+" * len(board[0]))
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * len(board[0]))

# Validate column input
def is_valid_input(input_char, cols):
    if len(input_char) != 1 or not input_char.isalpha():
        return False
    col_num = ord(input_char.upper()) - 65
    return 0 <= col_num < cols

# Place a checker in a column
def place_checker(board, checker, col):
    for row in reversed(board):
        if row[col] == " ":
            row[col] = checker
            return True
    return False

# Check for a win
def check_winner(board, checker):
    rows, cols = len(board), len(board[0])

    # Horizontal check
    for row in range(rows):
        for col in range(cols - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True

    # Vertical check
    for col in range(cols):
        for row in range(rows - 3):
            if all(board[row + i][col] == checker for i in range(4)):
                return True

    # Diagonal check (\)
    for row in range(rows - 3):
        for col in range(cols - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True

    # Diagonal check (/)
    for row in range(3, rows):
        for col in range(cols - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True

    return False

# Check for a draw
def check_draw(board):
    return all(cell != " " for row in board for cell in row)

# Main game function
def play_game(rows, cols, num_players):
    board = create_board(rows, cols)
    players = PLAYER_CHECKERS[:num_players]
    current_player_idx = random.randint(0, num_players - 1)

    print_board(board)
    while True:
        current_player = players[current_player_idx]
        print(f"Player {current_player}, please enter a column:")

        # Get valid column input
        while True:
            col_input = input("> ").strip()
            if not is_valid_input(col_input, cols):
                print("Invalid input. Please enter a valid column.")
                continue

            col = ord(col_input.upper()) - 65
            if not place_checker(board, current_player, col):
                print("Column is full. Please choose another column.")
            else:
                break

        print_board(board)

        # Check for win
        if check_winner(board, current_player):
            print(f"Player {current_player} won!")
            break

        # Check for draw
        if check_draw(board):
            print("It's a draw!")
            break

        # Switch to next player
        current_player_idx = (current_player_idx + 1) % num_players

# Entry point
if __name__ == "__main__":
    play_game(ROWS, COLS, 2)
