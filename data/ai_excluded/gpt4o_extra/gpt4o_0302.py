import os
import random

# Constants for the game configuration
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M'][:PLAYERS]

def create_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    os.system('clear')  # Clear the terminal screen
    column_labels = ' '.join(chr(i) for i in range(ord('A'), ord('A') + len(board[0])))
    print(f"  {column_labels}")
    print("+---" * len(board[0]) + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * len(board[0]) + "+")

def get_column_index(choice):
    if choice.isalpha() and (ord('A') <= ord(choice.upper()) < ord('A') + COLUMNS):
        return ord(choice.upper()) - ord('A')
    return -1

def is_valid_column(board, col):
    return 0 <= col < COLUMNS and board[0][col] == ' '

def place_checker(board, col, checker):
    for row in range(ROWS-1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = checker
            return True
    return False

def check_win(board, checker):
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col+i] == checker for i in range(4)):
                return True

    # Check vertical
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row+i][col] == checker for i in range(4)):
                return True

    # Check diagonals (bottom-left to top-right)
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row-i][col+i] == checker for i in range(4)):
                return True

    # Check diagonals (top-left to bottom-right)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row+i][col+i] == checker for i in range(4)):
                return True

    return False

def check_draw(board):
    return all(board[0][col] != ' ' for col in range(COLUMNS))

def connect_four():
    board = create_board(ROWS, COLUMNS)
    current_player = random.randint(0, PLAYERS - 1)

    print_board(board)

    while True:
        player_checker = CHECKERS[current_player]
        print(f"Player {player_checker}, please enter a column:")
        choice = input().strip().upper()
        col_index = get_column_index(choice)

        if col_index == -1 or not is_valid_column(board, col_index):
            print("Invalid choice, try again.")
            continue

        place_checker(board, col_index, player_checker)
        print_board(board)

        if check_win(board, player_checker):
            print(f"Player {player_checker} won!")
            break

        if check_draw(board):
            print("The game is a draw!")
            break

        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    connect_four()
