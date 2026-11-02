import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board(rows, columns):
    return [[' ' for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    os.system('clear')
    print("  " + "   ".join(chr(65 + i) for i in range(COLUMNS)))
    print("+---" * COLUMNS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

def get_valid_column(board):
    while True:
        col = input("Please enter a column: ").strip().upper()
        if col.isalpha() and len(col) == 1:
            col_index = ord(col) - 65
            if 0 <= col_index < COLUMNS and board[0][col_index] == ' ':
                return col_index
        print("Invalid input. Please try again.")

def place_checker(board, col, checker):
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = checker
            return

def check_winner(board, checker):
    # Horizontal, vertical
    for c in range(COLUMNS):
        for r in range(ROWS):
            if c <= COLUMNS - 4 and all(board[r][c + i] == checker for i in range(4)):
                return True
            if r <= ROWS - 4 and all(board[r + i][c] == checker for i in range(4)):
                return True
    # Diagonal
    for c in range(COLUMNS - 3):
        for r in range(ROWS - 3):
            if all(board[r + i][c + i] == checker for i in range(4)):
                return True
    for c in range(COLUMNS - 3):
        for r in range(3, ROWS):
            if all(board[r - i][c + i] == checker for i in range(4)):
                return True
    return False

def check_draw(board):
    return all(board[0][c] != ' ' for c in range(COLUMNS))

def play_game():
    board = create_board(ROWS, COLUMNS)
    current_player = random.randint(0, PLAYERS - 1)
    print_board(board)

    while True:
        print(f"Player {CHECKERS[current_player]}")
        col = get_valid_column(board)
        place_checker(board, col, CHECKERS[current_player])
        print_board(board)

        if check_winner(board, CHECKERS[current_player]):
            print(f"Player {CHECKERS[current_player]} won!")
            break
        elif check_draw(board):
            print("The game is a draw!")
            break

        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    play_game()
