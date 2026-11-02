import os
import random

# Constants for the game setup
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
PLAYERS_CHECKERS = ["X", "O", "V", "H", "M"]

def create_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')  # Clear the console
    print("  " + "   ".join(chr(65 + i) for i in range(COLUMNS)))  # Column labels A-G
    print("+---" * COLUMNS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

def is_valid_input(column, board):
    if len(column) != 1 or column not in [chr(65 + i) for i in range(COLUMNS)]:
        return False
    col_index = ord(column) - 65
    return board[0][col_index] == " "

def find_row(board, column):
    col_index = ord(column) - 65
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_index] == " ":
            return row
    return -1  # Column is full

def place_checker(board, column, checker):
    row = find_row(board, column)
    if row != -1:
        col_index = ord(column) - 65
        board[row][col_index] = checker
        return True
    return False

def check_winner(board, checker):
    # Check horizontal, vertical and diagonal for a win
    for r in range(ROWS):
        for c in range(COLUMNS):
            if (c + 3 < COLUMNS and all(board[r][c+i] == checker for i in range(4))) or \
               (r + 3 < ROWS and all(board[r+i][c] == checker for i in range(4))) or \
               (r + 3 < ROWS and c + 3 < COLUMNS and all(board[r+i][c+i] == checker for i in range(4))) or \
               (r - 3 >= 0 and c + 3 < COLUMNS and all(board[r-i][c+i] == checker for i in range(4))):
                return True
    return False

def check_draw(board):
    return all(board[0][col] != " " for col in range(COLUMNS))

def main():
    board = create_board()
    num_players = 2  # Set to 2 players for submission
    players = PLAYERS_CHECKERS[:num_players]
    current_player_index = random.randint(0, num_players - 1)

    print_board(board)
    
    while True:
        current_checker = players[current_player_index]
        column = input(f"Player {current_checker}, please enter a column: ").upper()

        while not is_valid_input(column, board):
            print("Invalid input. Please try again.")
            column = input(f"Player {current_checker}, please enter a column: ").upper()

        place_checker(board, column, current_checker)
        print_board(board)

        if check_winner(board, current_checker):
            print(f"Player {current_checker} won!")
            break
        if check_draw(board):
            print("The game is a draw!")
            break

        current_player_index = (current_player_index + 1) % num_players

if __name__ == "__main__":
    main()
