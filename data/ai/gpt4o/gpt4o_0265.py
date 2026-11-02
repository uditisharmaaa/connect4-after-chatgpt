import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS_COUNT = 2
CHECKERS = ["X", "O", "V", "H", "M"]
MAX_COLS = 26

# Initialize the board
def create_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

# Print the board
def print_board(board):
    os.system('clear')
    
    # Column headers
    print("  " + "   ".join(chr(i) for i in range(65, 65 + COLUMNS)))
    print("+" + "---+" * COLUMNS)
    
    # Rows
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLUMNS)

# Check if the input is valid
def valid_input(input_char):
    if len(input_char) == 1 and input_char.isalpha():
        column_index = ord(input_char.upper()) - 65
        return 0 <= column_index < COLUMNS
    return False

# Place the checker in the correct position
def place_checker(board, checker, column):
    column_index = ord(column.upper()) - 65
    for row in reversed(board):
        if row[column_index] == " ":
            row[column_index] = checker
            return True
    return False

# Check for win condition
def check_win(board, checker):
    # Check horizontally
    for row in board:
        for col in range(COLUMNS - 3):
            if row[col] == checker and row[col + 1] == checker and row[col + 2] == checker and row[col + 3] == checker:
                return True

    # Check vertically
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if board[row][col] == checker and board[row + 1][col] == checker and board[row + 2][col] == checker and board[row + 3][col] == checker:
                return True

    # Check diagonally (descending)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if board[row][col] == checker and board[row + 1][col + 1] == checker and board[row + 2][col + 2] == checker and board[row + 3][col + 3] == checker:
                return True

    # Check diagonally (ascending)
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if board[row][col] == checker and board[row - 1][col + 1] == checker and board[row - 2][col + 2] == checker and board[row - 3][col + 3] == checker:
                return True

    return False

# Check for a draw condition
def check_draw(board):
    return all(all(cell != " " for cell in row) for row in board)

def play_game():
    board = create_board()
    print_board(board)

    current_player = random.randint(0, PLAYERS_COUNT - 1)

    while True:
        current_checker = CHECKERS[current_player]

        # Prompt player input
        column_choice = input(f"Player {current_checker}, please enter a column: ").strip()
        while not valid_input(column_choice) or not place_checker(board, current_checker, column_choice):
            column_choice = input(f"Invalid input. Player {current_checker}, please enter a valid column: ").strip()
        
        print_board(board)

        # Check for win
        if check_win(board, current_checker):
            print(f"Player {current_checker} won!")
            break

        # Check for draw
        if check_draw(board):
            print("The game is a draw!")
            break

        # Switch player
        current_player = (current_player + 1) % PLAYERS_COUNT

if __name__ == "__main__":
    play_game()
