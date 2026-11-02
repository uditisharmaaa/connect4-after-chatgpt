import os
import random

# Configuration constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

# Clear the console screen
def clear_screen():
    os.system('clear')

# Initialize the board
def create_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

# Print the board
def print_board(board):
    clear_screen()
    # Print column labels
    col_labels = '  ' + '   '.join(chr(65 + i) for i in range(COLS))
    print(col_labels)
    print("+---" * COLS + "+")
    # Print each row
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLS + "+")

# Place checker in column
def place_checker(board, column, checker):
    for i in range(ROWS - 1, -1, -1):
        if board[i][column] == ' ':
            board[i][column] = checker
            return True
    return False

# Check if the input is valid
def is_valid_input(input_str):
    if len(input_str) != 1:
        return False
    upper_input = input_str.upper()
    return 'A' <= upper_input <= chr(65 + COLS - 1)

# Check for a win
def check_win(board, checker):
    # Horizontal check
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True
    
    # Vertical check
    for col in range(COLS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == checker for i in range(4)):
                return True

    # Diagonal check (/)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True

    # Diagonal check (\)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True

    return False

# Check for a draw
def check_draw(board):
    for row in board:
        if ' ' in row:
            return False
    return True

# Main game loop
def connect4():
    board = create_board(ROWS, COLS)
    current_player_index = random.randint(0, PLAYERS - 1)
    print_board(board)

    while True:
        current_checker = CHECKERS[current_player_index]
        player_input = input(f"Player {current_checker}, please enter a column: ")

        if not is_valid_input(player_input):
            print("Invalid input. Please enter a valid column (A-G).")
            continue

        column = ord(player_input.upper()) - 65

        if not place_checker(board, column, current_checker):
            print("Column is full. You lose the turn.")
            current_player_index = (current_player_index + 1) % PLAYERS
            continue

        print_board(board)

        if check_win(board, current_checker):
            print(f"Player {current_checker} won!")
            break
        elif check_draw(board):
            print("The game is a draw!")
            break

        current_player_index = (current_player_index + 1) % PLAYERS

connect4()
