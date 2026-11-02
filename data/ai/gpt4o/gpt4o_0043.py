import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']  # Support for up to 5 players

def create_board(rows, columns):
    return [[' ' for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    os.system('clear')
    column_labels = ' '.join(chr(i + ord('A')) for i in range(len(board[0])))
    print(f"  {column_labels}")
    for row in board:
        print("+---" * len(row) + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * len(board[0]) + "+")

def is_valid_column(column, board):
    if column < 'A' or column >= chr(ord('A') + len(board[0])):
        return False
    column_index = ord(column) - ord('A')
    return board[0][column_index] == ' '

def get_next_open_row(board, column):
    column_index = ord(column) - ord('A')
    for r in range(len(board) - 1, -1, -1):
        if board[r][column_index] == ' ':
            return r
    return None

def place_checker(board, row, column, checker):
    column_index = ord(column) - ord('A')
    board[row][column_index] = checker

def check_for_win(board, checker):
    # Horizontal check
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col+i] == checker for i in range(4)):
                return True

    # Vertical check
    for row in range(ROWS - 3):
        for col in range(COLUMNS):
            if all(board[row+i][col] == checker for i in range(4)):
                return True

    # Diagonal checks
    # Positive diagonal
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row+i][col+i] == checker for i in range(4)):
                return True

    # Negative diagonal
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row-i][col+i] == checker for i in range(4)):
                return True

    return False

def check_for_draw(board):
    return all(board[0][col] != ' ' for col in range(COLUMNS))

def play_game():
    board = create_board(ROWS, COLUMNS)
    print_board(board)

    current_player = random.randint(0, PLAYERS - 1)
    while True:
        print(f"Player {CHECKERS[current_player]}, please enter a column:")
        
        column = input().strip().upper()
        while not is_valid_column(column, board):
            print("Invalid column. Please enter a valid column:")
            column = input().strip().upper()

        row = get_next_open_row(board, column)
        if row is not None:
            place_checker(board, row, column, CHECKERS[current_player])
            print_board(board)

            if check_for_win(board, CHECKERS[current_player]):
                print(f"Player {CHECKERS[current_player]} won!")
                break

            if check_for_draw(board):
                print("The game is a draw!")
                break

            current_player = (current_player + 1) % PLAYERS
        else:
            print("Column is full. Choose another column.")

if __name__ == "__main__":
    play_game()
