import random
import os

# Constants
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']
NUM_PLAYERS = 2  # You can change this between 2 and 5

def create_board():
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    print("  " + "   ".join(chr(65 + i) for i in range(COLUMNS)))
    print("+" + "---+" * COLUMNS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLUMNS)

def get_column_index(column):
    return ord(column.upper()) - 65

def is_valid_column(column, board):
    if len(column) != 1 or not column.isalpha():
        return False
    index = get_column_index(column)
    return 0 <= index < COLUMNS and board[0][index] == ' '

def make_move(board, column, symbol):
    col_index = get_column_index(column)
    for row in reversed(board):
        if row[col_index] == ' ':
            row[col_index] = symbol
            break

def check_win(board, symbol):
    # Check horizontal
    for row in board:
        for col in range(COLUMNS - 3):
            if all(row[col+i] == symbol for i in range(4)):
                return True
    # Check vertical
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row+i][col] == symbol for i in range(4)):
                return True
    # Check diagonal (/)
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row-i][col+i] == symbol for i in range(4)):
                return True
    # Check diagonal (\)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row+i][col+i] == symbol for i in range(4)):
                return True
    return False

def is_draw(board):
    return all(cell != ' ' for row in board for cell in row)

def connect_4():
    board = create_board()
    players = PLAYER_SYMBOLS[:NUM_PLAYERS]
    current_player = random.choice(players)
    print_board(board)

    while True:
        column = input(f"Player {current_player}, please enter a column: ")
        while not is_valid_column(column, board):
            column = input("Invalid column. Please enter another column: ")

        make_move(board, column, current_player)
        print_board(board)

        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            break
        if is_draw(board):
            print("The game is a draw!")
            break

        current_player = players[(players.index(current_player) + 1) % NUM_PLAYERS]

if __name__ == "__main__":
    connect_4()
