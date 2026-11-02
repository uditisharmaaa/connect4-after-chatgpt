import os
import random
import string

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
SYMBOLS = ["X", "O", "V", "H", "M"]

def create_board(rows, columns):
    """Creates and returns a board initialized with empty spaces."""
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    """Prints the board to the console."""
    os.system('clear')
    header = "  " + "   ".join(string.ascii_uppercase[:len(board[0])]) + "  "
    separator = "+---" * len(board[0]) + "+"
    
    print(header)
    for row in board:
        print(separator)
        print("| " + " | ".join(row) + " |")
    print(separator)

def is_valid_column(input_char, columns):
    """Checks if the input character corresponds to a valid column."""
    return input_char in string.ascii_uppercase[:columns]

def get_next_open_row(board, col):
    """Returns the index of the next available row in the specified column."""
    for r in reversed(range(len(board))):
        if board[r][col] == " ":
            return r
    return -1

def place_checker(board, col, symbol):
    """Places the player's checker in the specified column."""
    row = get_next_open_row(board, col)
    if row != -1:
        board[row][col] = symbol
    return row

def check_winner(board, symbol):
    """Checks board for a win by the specified symbol."""
    # Check horizontal
    for r in range(ROWS):
        for c in range(COLUMNS - 3):
            if all(board[r][c+i] == symbol for i in range(4)):
                return True

    # Check vertical
    for r in range(ROWS - 3):
        for c in range(COLUMNS):
            if all(board[r+i][c] == symbol for i in range(4)):
                return True

    # Check positively sloped diagonals
    for r in range(ROWS - 3):
        for c in range(COLUMNS - 3):
            if all(board[r+i][c+i] == symbol for i in range(4)):
                return True

    # Check negatively sloped diagonals
    for r in range(3, ROWS):
        for c in range(COLUMNS - 3):
            if all(board[r-i][c+i] == symbol for i in range(4)):
                return True

    return False

def is_draw(board):
    """Checks if the board is completely filled."""
    return all(board[0][c] != " " for c in range(COLUMNS))

def play():
    """Main function to play Connect 4 game."""
    board = create_board(ROWS, COLUMNS)
    player_symbols = SYMBOLS[:PLAYERS]
    current_player = random.randint(0, PLAYERS - 1)

    print_board(board)

    while True:
        current_symbol = player_symbols[current_player]
        print(f"Player {current_symbol}, please enter a column:")

        while True:
            col_input = input().strip().upper()
            if is_valid_column(col_input, COLUMNS):
                col = string.ascii_uppercase.index(col_input)
                if get_next_open_row(board, col) != -1:
                    break
                else:
                    print("Column is full! Please choose another column.")
            else:
                print("Invalid input! Please enter a valid column letter.")

        place_checker(board, col, current_symbol)
        print_board(board)

        if check_winner(board, current_symbol):
            print(f"Player {current_symbol} won!")
            break
        elif is_draw(board):
            print("The game is a draw!")
            break

        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    play()
