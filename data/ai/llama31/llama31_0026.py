import os
import random

# Constant variables for board dimensions and number of players
BOARD_ROWS = 6
BOARD_COLS = 7
NUM_PLAYERS = 2

# List of checkers for players
CHECKERS = ["X", "O", "V", "H", "M"]

# Initialize the board with whitespaces
def initialize_board():
    board = []
    for _ in range(BOARD_ROWS):
        row = []
        for _ in range(BOARD_COLS):
            row.append(" ")
        board.append(row)
    return board

# Print the board
def print_board(board):
    os.system('clear')
    print("  A   B   C   D   E   F   G")
    for row in board:
        print("+---+---+---+---+---+---+---+")
        row_str = ""
        for cell in row:
            row_str += "| " + cell + " "
        row_str += "|"
        print(row_str)
    print("+---+---+---+---+---+---+---+")

# Randomly select the first player
def select_first_player():
    return random.randint(0, NUM_PLAYERS - 1)

# Validate user input
def validate_input(board, column):
    if not column.isalpha() or column.upper() not in "ABCDEFG":
        return False
    column_index = ord(column.upper()) - ord('A')
    if board[0][column_index]!= " ":
        return False
    return True

# Place the checker at the correct location
def place_checker(board, column, checker):
    column_index = ord(column.upper()) - ord('A')
    for row in reversed(board):
        if row[column_index] == " ":
            row[column_index] = checker
            break

# Check for a win
def check_win(board, checker):
    # Check horizontal locations for win
    for c in range(BOARD_COLS - 3):
        for r in range(BOARD_ROWS):
            if board[r][c] == checker and board[r][c + 1] == checker and board[r][c + 2] == checker and board[r][c + 3] == checker:
                return True

    # Check vertical locations for win
    for c in range(BOARD_COLS):
        for r in range(BOARD_ROWS - 3):
            if board[r][c] == checker and board[r + 1][c] == checker and board[r + 2][c] == checker and board[r + 3][c] == checker:
                return True

    # Check positively sloped diagonals
    for c in range(BOARD_COLS - 3):
        for r in range(BOARD_ROWS - 3):
            if board[r][c] == checker and board[r + 1][c + 1] == checker and board[r + 2][c + 2] == checker and board[r + 3][c + 3] == checker:
                return True

    # Check negatively sloped diagonals
    for c in range(BOARD_COLS - 3):
        for r in range(3, BOARD_ROWS):
            if board[r][c] == checker and board[r - 1][c + 1] == checker and board[r - 2][c + 2] == checker and board[r - 3][c + 3] == checker:
                return True

    return False

# Check for a draw
def check_draw(board):
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True

# Main game loop
def game():
    board = initialize_board()
    current_player = select_first_player()
    print_board(board)

    while True:
        column = input(f"Player {CHECKERS[current_player]}, please enter a column: ").strip().upper()
        while not validate_input(board, column):
            column = input(f"Invalid input. Please enter a column: ").strip().upper()

        place_checker(board, column, CHECKERS[current_player])
        print_board(board)

        if check_win(board, CHECKERS[current_player]):
            print(f"Player {CHECKERS[current_player]} won!")
            break

        if check_draw(board):
            print("It's a draw!")
            break

        current_player = (current_player + 1) % NUM_PLAYERS

game()
