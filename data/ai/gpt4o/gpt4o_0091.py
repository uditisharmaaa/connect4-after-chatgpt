import os
import random

# Constants for board dimensions and number of players
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

# Initialize the board
def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

# Print the current state of the board
def print_board(board):
    os.system('clear')
    print("  " + "   ".join(chr(65 + i) for i in range(len(board[0]))))
    print("+---" * len(board[0]) + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * len(board[0]) + "+")

# Check if the input column is valid
def valid_column_input(input_char, board):
    if len(input_char) != 1 or not input_char.isalpha():
        return False
    col_index = ord(input_char.upper()) - 65
    return 0 <= col_index < len(board[0]) and board[0][col_index] == " "

# Place the checker in the correct location
def place_checker(board, col, player_checker):
    col_index = ord(col.upper()) - 65
    for row in reversed(board):
        if row[col_index] == " ":
            row[col_index] = player_checker
            return

# Check for a win condition
def check_win(board, player_checker):
    # Check horizontally, vertically, and diagonally

    # Horizontal check
    for row in board:
        for start in range(COLS - 3):
            if all(row[start + i] == player_checker for i in range(4)):
                return True

    # Vertical check
    for col in range(COLS):
        for start in range(ROWS - 3):
            if all(board[start + i][col] == player_checker for i in range(4)):
                return True

    # Diagonal checks (both directions)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == player_checker for i in range(4)):
                return True
            if all(board[row + 3 - i][col + i] == player_checker for i in range(4)):
                return True

    return False

# Check for a draw condition
def check_draw(board):
    return all(cell != " " for row in board for cell in row)

# Main game function
def connect_4():
    board = create_board(ROWS, COLS)
    current_player = random.choice(range(PLAYERS))
    print_board(board)

    while True:
        current_checker = CHECKERS[current_player]
        print(f"Player {current_checker}, please enter a column:")
        while True:
            user_input = input().strip()
            if valid_column_input(user_input, board):
                place_checker(board, user_input, current_checker)
                break
            else:
                print("Invalid input. Please enter a valid column:")

        print_board(board)

        # Check for win or draw
        if check_win(board, current_checker):
            print(f"Player {current_checker} won!")
            break
        elif check_draw(board):
            print("The game is a draw!")
            break

        # Switch players
        current_player = (current_player + 1) % PLAYERS

# Run the game
if __name__ == "__main__":
    connect_4()
