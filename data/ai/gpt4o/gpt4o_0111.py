import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"][:PLAYERS]

def create_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    print("  " + "   ".join(chr(65 + i) for i in range(COLUMNS)))
    print("+" + "---+" * COLUMNS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLUMNS)

def valid_input(input_col):
    return input_col.isalpha() and input_col.upper() in list(map(chr, range(65, 65 + COLUMNS)))

def drop_checker(board, col, checker):
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    return False

def check_for_win(board, checker):
    # Horizontal
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if board[row][col] == checker and all(board[row][col + i] == checker for i in range(1, 4)):
                return True
    
    # Vertical
    for row in range(ROWS - 3):
        for col in range(COLUMNS):
            if board[row][col] == checker and all(board[row + i][col] == checker for i in range(1, 4)):
                return True
    
    # Diagonal (top-left to bottom-right)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if board[row][col] == checker and all(board[row + i][col + i] == checker for i in range(1, 4)):
                return True
    
    # Diagonal (bottom-left to top-right)
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if board[row][col] == checker and all(board[row - i][col + i] == checker for i in range(1, 4)):
                return True
    
    return False

def board_full(board):
    return all(board[row][col] != " " for col in range(COLUMNS) for row in range(ROWS))

def play_game():
    board = create_board()
    current_player = random.randint(0, PLAYERS - 1)
    print_board(board)

    while True:
        print(f"Player {CHECKERS[current_player]}, please enter a column:")
        input_col = input().strip()

        while not valid_input(input_col):
            print("Invalid input. Please enter a valid column:")
            input_col = input().strip()        
        col = ord(input_col.upper()) - 65

        if not drop_checker(board, col, CHECKERS[current_player]):
            print(f"Column {input_col.upper()} is full. Turn is lost.")
        else:
            print_board(board)
            if check_for_win(board, CHECKERS[current_player]):
                print(f"Player {CHECKERS[current_player]} won!")
                break
            if board_full(board):
                print("The game is a draw!")
                break
            current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    play_game()
