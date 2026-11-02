import os
import random

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
MAX_PLAYERS = 5
CHECKERS = ["X", "O", "V", "H", "M"]

# Initialize the board with whitespaces
def create_board():
    return [[" " for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

# Print the board with column labels
def print_board(board):
    print("  A   B   C   D   E   F   G")
    for row in board:
        print("+---" * BOARD_COLS + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * BOARD_COLS + "+")

# Randomly select the first player
def select_first_player(num_players):
    return random.randint(0, num_players - 1)

# Validate user input
def validate_input(column, num_cols):
    if not column.isalpha():
        return False
    column = ord(column.upper()) - 65
    return 0 <= column < num_cols

# Get the next available row in a column
def get_next_row(board, column):
    for row in reversed(board):
        if row[column] == " ":
            return board.index(row)
    return -1

# Check for a win
def check_win(board, player_checker):
    # Check horizontal wins
    for row in board:
        for col in range(len(row) - 3):
            if row[col] == row[col + 1] == row[col + 2] == row[col + 3] == player_checker:
                return True

    # Check vertical wins
    for col in range(len(board[0])):
        for row in range(len(board) - 3):
            if board[row][col] == board[row + 1][col] == board[row + 2][col] == board[row + 3][col] == player_checker:
                return True

    # Check diagonal wins (top-left to bottom-right)
    for row in range(len(board) - 3):
        for col in range(len(board[0]) - 3):
            if board[row][col] == board[row + 1][col + 1] == board[row + 2][col + 2] == board[row + 3][col + 3] == player_checker:
                return True

    # Check diagonal wins (bottom-left to top-right)
    for row in range(3, len(board)):
        for col in range(len(board[0]) - 3):
            if board[row][col] == board[row - 1][col + 1] == board[row - 2][col + 2] == board[row - 3][col + 3] == player_checker:
                return True

    return False

# Check for a draw
def check_draw(board):
    return all(cell!= " " for row in board for cell in row)

# Main game loop
def play_game():
    num_players = 2
    board = create_board()
    current_player = select_first_player(num_players)
    checkers = CHECKERS[:num_players]

    while True:
        os.system('clear')
        print_board(board)
        print("Player", checkers[current_player], "turn. Please enter a column (A-G):")

        while True:
            column = input().upper()
            if validate_input(column, BOARD_COLS):
                column = ord(column) - 65
                next_row = get_next_row(board, column)
                if next_row!= -1:
                    board[next_row][column] = checkers[current_player]
                    break
                else:
                    print("Column is full. Please try again.")
            else:
                print("Invalid input. Please try again.")

        if check_win(board, checkers[current_player]):
            os.system('clear')
            print_board(board)
            print("Player", checkers[current_player], "won!")
            break

        if check_draw(board):
            os.system('clear')
            print_board(board)
            print("It's a draw!")
            break

        current_player = (current_player + 1) % num_players

play_game()
