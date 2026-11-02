import random
import os

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    print("  " + "   ".join(chr(ord('A') + i) for i in range(COLUMNS)))
    for row in board:
        print("+---" * COLUMNS + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * COLUMNS + "+")

def is_valid_input(input_col):
    return input_col.isalpha() and 'A' <= input_col < chr(ord('A') + COLUMNS)

def place_checker(board, col, checker):
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = checker
            return True
    return False

def check_win(board, checker):
    # Check horizontal
    for row in board:
        for col in range(COLUMNS - 3):
            if all(row[col+i] == checker for i in range(4)):
                return True

    # Check vertical
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row+i][col] == checker for i in range(4)):
                return True

    # Check diagonal (bottom-left to top-right)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row+i][col+i] == checker for i in range(4)):
                return True

    # Check diagonal (top-left to bottom-right)
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row-i][col+i] == checker for i in range(4)):
                return True

    return False

def check_draw(board):
    return all(cell != ' ' for row in board for cell in row)

def play_game():
    board = create_board()
    current_player = random.randint(0, PLAYERS - 1)
    
    print_board(board)

    while True:
        checker = CHECKERS[current_player]
        column_letter = input(f"Player {checker}, please enter a column: ").upper()
        
        if not is_valid_input(column_letter):
            print("Invalid input. Please enter a valid column.")
            continue
        
        col = ord(column_letter) - ord('A')
        
        if not place_checker(board, col, checker):
            print(f"Column {column_letter} is full. Turn lost.")
            current_player = (current_player + 1) % PLAYERS
            continue
        
        print_board(board)

        if check_win(board, checker):
            print(f"Player {checker} won!")
            break
        
        if check_draw(board):
            print("The game is a draw!")
            break
        
        current_player = (current_player + 1) % PLAYERS

play_game()
