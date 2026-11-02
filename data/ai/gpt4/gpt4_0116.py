import random
import os

# Constants
ROWS = 6
COLUMNS = 7
MAX_COLUMNS = 26
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

# Create the board and initialize it with spaces
def create_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]

# Print the board to the console
def print_board(board):
    os.system('clear')  # Clear the screen
    column_labels = [chr(65 + i) for i in range(len(board[0]))]
    print("  " + "   ".join(column_labels))
    print("+---" * len(board[0]) + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * len(board[0]) + "+")

# Check if the column input is valid
def is_valid_column(input_char, board):
    if len(input_char) != 1 or not input_char.isalpha():
        return False
    col_index = ord(input_char.upper()) - 65
    if 0 <= col_index < len(board[0]) and board[0][col_index] == " ":
        return True
    return False

# Place a checker into the correct column
def place_checker(board, column, checker):
    col_index = ord(column.upper()) - 65
    for row in reversed(board):
        if row[col_index] == " ":
            row[col_index] = checker
            break

# Check for a win
def check_win(board, checker):
    num_rows = len(board)
    num_cols = len(board[0])

    # Check horizontal wins
    for row in range(num_rows):
        for col in range(num_cols - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True

    # Check vertical wins
    for row in range(num_rows - 3):
        for col in range(num_cols):
            if all(board[row + i][col] == checker for i in range(4)):
                return True

    # Check right diagonal wins
    for row in range(num_rows - 3):
        for col in range(num_cols - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True

    # Check left diagonal wins
    for row in range(num_rows - 3):
        for col in range(3, num_cols):
            if all(board[row + i][col - i] == checker for i in range(4)):
                return True

    return False

# Check if the board is full
def is_draw(board):
    return all(cell != " " for row in board for cell in row)

# Game loop
def play_game(rows, columns, players):
    board = create_board(rows, columns)
    current_player_index = random.randint(0, players - 1)
    player_checkers = CHECKERS[:players]

    while True:
        print_board(board)
        current_player_checker = player_checkers[current_player_index]
        print(f"Player {current_player_checker}, it's your turn!")
        
        # Get and validate user input
        while True:
            user_input = input("Please enter a column: ").strip().upper()
            if is_valid_column(user_input, board):
                break
            print("Invalid input. Try again.")

        # Place checker
        place_checker(board, user_input, current_player_checker)

        # Check for a win
        if check_win(board, current_player_checker):
            print_board(board)
            print(f"Player {current_player_checker} won!")
            break

        # Check for a draw
        if is_draw(board):
            print_board(board)
            print("It's a draw!")
            break

        # Switch to the next player
        current_player_index = (current_player_index + 1) % players

# Main entry point
if __name__ == "__main__":
    play_game(ROWS, COLUMNS, PLAYERS)
