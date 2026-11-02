import random
import os

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
SYMBOLS = ["X", "O", "V", "H", "M"][:PLAYERS]

# Initialize the board
def create_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]

# Print the board
def print_board(board):
    os.system('clear')
    headers = "  " + "   ".join(chr(65 + i) for i in range(len(board[0])))
    print(headers)
    print("+---" * len(board[0]) + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * len(board[0]) + "+")

# Validate input
def validate_input(choice, board):
    return choice.isalpha() and 'A' <= choice <= chr(65 + len(board[0]) - 1)

# Drop checker
def drop_checker(board, column, symbol):
    for row in reversed(board):
        if row[column] == " ":
            row[column] = symbol
            return True
    return False

# Check for win
def check_win(board, symbol):
    # Check horizontal, vertical and diagonal lines
    for row in range(ROWS):
        for col in range(COLUMNS):
            if all(row + i < ROWS and board[row + i][col] == symbol for i in range(4)):
                return True
            if all(col + i < COLUMNS and board[row][col + i] == symbol for i in range(4)):
                return True
            if all(row + i < ROWS and col + i < COLUMNS and board[row + i][col + i] == symbol for i in range(4)):
                return True
            if all(row + i < ROWS and col - i >= 0 and board[row + i][col - i] == symbol for i in range(4)):
                return True
    return False

# Check for draw
def check_draw(board):
    return all(cell != " " for row in board for cell in row)

# Main game loop
def play_game():
    board = create_board(ROWS, COLUMNS)
    current_player = random.choice(SYMBOLS)
    while True:
        print_board(board)
        choice = input(f"Player {current_player}, please enter a column: ").upper()

        if not validate_input(choice, board):
            print("Invalid input. Try again.")
            continue

        column_index = ord(choice) - 65
        if not drop_checker(board, column_index, current_player):
            print("Column full. Turn lost.")
            current_player = SYMBOLS[(SYMBOLS.index(current_player) + 1) % PLAYERS]
            continue

        if check_win(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break

        if check_draw(board):
            print_board(board)
            print("The game is a draw!")
            break

        current_player = SYMBOLS[(SYMBOLS.index(current_player) + 1) % PLAYERS]

play_game()
