import random
import os

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']
BOARD_EMPTY_CELL = " "

def init_board(rows, cols):
    return [[BOARD_EMPTY_CELL for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    os.system('clear')
    print("  " + "   ".join(chr(65 + i) for i in range(COLUMNS)))
    print("+---" * COLUMNS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

def is_valid_input(column):
    return column.isalpha() and 0 <= ord(column.upper()) - 65 < COLUMNS

def get_lowest_empty_row(board, column):
    for row in range(ROWS-1, -1, -1):
        if board[row][column] == BOARD_EMPTY_CELL:
            return row
    return None

def check_win(board, checker):
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True
    # Check vertical
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == checker for i in range(4)):
                return True
    # Check diagonal /
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True
    # Check diagonal \
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True
    return False

def check_draw(board):
    return all(board[0][col] != BOARD_EMPTY_CELL for col in range(COLUMNS))

def main():
    board = init_board(ROWS, COLUMNS)
    print_board(board)
    current_player = random.choice(range(PLAYERS))
    while True:
        print(f"Player {CHECKERS[current_player]}, please enter a column:")
        while True:
            user_input = input().strip().upper()
            if is_valid_input(user_input):
                column = ord(user_input) - 65
                row = get_lowest_empty_row(board, column)
                if row is not None:
                    board[row][column] = CHECKERS[current_player]
                    break
                else:
                    print("Column is full. Choose another column.")
            else:
                print("Invalid input. Please enter a valid column letter.")
        print_board(board)
        if check_win(board, CHECKERS[current_player]):
            print(f"Player {CHECKERS[current_player]} won!")
            break
        if check_draw(board):
            print("The game is a draw!")
            break
        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
