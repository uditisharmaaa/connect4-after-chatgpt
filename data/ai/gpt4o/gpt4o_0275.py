import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
PIECES = ["X", "O", "V", "H", "M"]

# Functions
def clear_screen():
    os.system('clear')

def initialize_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    print("  " + "   ".join(chr(65 + i) for i in range(COLUMNS)))
    print("+---" * COLUMNS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

def column_to_index(column_letter):
    if column_letter in [chr(i) for i in range(65, 65 + COLUMNS)]:
        return ord(column_letter) - 65
    return -1

def get_valid_column(board, current_player):
    while True:
        column_letter = input(f"Player {PIECES[current_player]}, please enter a column: ").strip().upper()
        column_index = column_to_index(column_letter)
        if column_index == -1:
            print("Invalid column. Try again.")
        elif board[0][column_index] != " ":
            print("Column full. Cannot place piece here.")
        else:
            return column_index

def place_piece(board, column_index, piece):
    for row_index in range(ROWS-1, -1, -1):
        if board[row_index][column_index] == " ":
            board[row_index][column_index] = piece
            return

def check_win(board, piece):
    # Horizontal check
    for row in board:
        for col in range(COLUMNS - 3):
            if all(cell == piece for cell in row[col:col+4]):
                return True

    # Vertical check
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row+i][col] == piece for i in range(4)):
                return True

    # Diagonal checks
    # Bottom-left to top-right
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row+i][col+i] == piece for i in range(4)):
                return True
    # Top-left to bottom-right
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row-i][col+i] == piece for i in range(4)):
                return True
    
    return False

def check_draw(board):
    return all(board[0][col] != " " for col in range(COLUMNS))

def play_game():
    board = initialize_board(ROWS, COLUMNS)
    num_players = 2
    current_player = random.randint(0, num_players - 1)

    print_board(board)

    while True:
        column_index = get_valid_column(board, current_player)
        place_piece(board, column_index, PIECES[current_player])
        print_board(board)

        if check_win(board, PIECES[current_player]):
            print(f"Player {PIECES[current_player]} won!")
            break
        elif check_draw(board):
            print("The game is a draw!")
            break

        current_player = (current_player + 1) % num_players

play_game()
