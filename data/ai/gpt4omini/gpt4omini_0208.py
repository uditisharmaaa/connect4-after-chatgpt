import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]

def create_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')  # Clear the console (Linux/Unix)
    print("  " + "   ".join(chr(65 + i) for i in range(COLUMNS)))
    print("+" + "---+" * COLUMNS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLUMNS)

def is_valid_input(column):
    return column.isalpha() and len(column) == 1 and 'A' <= column.upper() <= chr(64 + COLUMNS)

def get_col_index(column):
    return ord(column.upper()) - 65

def is_column_full(board, col):
    return board[0][col] != " "

def place_checker(board, col, checker):
    for row in reversed(board):
        if row[col] == " ":
            row[col] = checker
            return True
    return False

def check_win(board, checker):
    # Check horizontal, vertical and diagonal
    for row in range(ROWS):
        for col in range(COLUMNS):
            if (col <= COLUMNS - 4 and all(board[row][col + i] == checker for i in range(4))) or \
               (row <= ROWS - 4 and all(board[row + i][col] == checker for i in range(4))) or \
               (row <= ROWS - 4 and col <= COLUMNS - 4 and all(board[row + i][col + i] == checker for i in range(4))) or \
               (row >= 3 and col <= COLUMNS - 4 and all(board[row - i][col + i] == checker for i in range(4))):
                return True
    return False

def check_draw(board):
    return all(board[0][col] != " " for col in range(COLUMNS))

def main():
    board = create_board()
    players = min(len(PLAYER_SYMBOLS), 5)  # Allow up to 5 players
    current_player = random.randint(0, players - 1)

    print_board(board)
    while True:
        checker = PLAYER_SYMBOLS[current_player]
        valid_input = False

        while not valid_input:
            column = input(f"Player {checker}, please enter a column: ")
            if is_valid_input(column):
                col_index = get_col_index(column)
                if not is_column_full(board, col_index):
                    place_checker(board, col_index, checker)
                    valid_input = True
                else:
                    print(f"Column {column.upper()} is full; choose another column.")
            else:
                print("Invalid input. Please enter a letter A-G.")

        print_board(board)

        if check_win(board, checker):
            print(f"Player {checker} won!")
            break
        if check_draw(board):
            print("The game is a draw.")
            break
        
        current_player = (current_player + 1) % players

if __name__ == "__main__":
    main()
