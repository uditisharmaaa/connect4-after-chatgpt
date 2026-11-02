import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"][:PLAYERS]

def print_board(board):
    os.system('clear')
    print("  " + "   ".join(chr(ord('A') + i) for i in range(COLUMNS)))
    print("+---" * COLUMNS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

def create_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def is_valid_input(input, board):
    if len(input) == 1 and 'A' <= input <= chr(ord('A') + COLUMNS - 1):
        column = ord(input) - ord('A')
        if board[0][column] == " ":
            return True
    return False

def make_move(board, column, checker):
    for row in reversed(range(ROWS)):
        if board[row][column] == " ":
            board[row][column] = checker
            return

def check_winner(board, checker):
    # Horizontal check
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if board[row][col:col + 4] == [checker] * 4:
                return True
    
    # Vertical check
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == checker for i in range(4)):
                return True

    # Diagonal checks
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True
        for col in range(3, COLUMNS):
            if all(board[row + i][col - i] == checker for i in range(4)):
                return True

    return False

def check_draw(board):
    return all(board[0][col] != " " for col in range(COLUMNS))

def play_game():
    board = create_board()
    current_player = random.randint(0, PLAYERS - 1)
    print_board(board)

    while True:
        print(f"Player {CHECKERS[current_player]}, please enter a column:")
        column_input = input().strip().upper()

        if not is_valid_input(column_input, board):
            print("Invalid input. Try again.")
            continue
        
        column = ord(column_input) - ord('A')
        make_move(board, column, CHECKERS[current_player])
        print_board(board)

        if check_winner(board, CHECKERS[current_player]):
            print(f"Player {CHECKERS[current_player]} won!")
            break
        
        if check_draw(board):
            print("The game is a draw!")
            break

        current_player = (current_player + 1) % PLAYERS

play_game()
