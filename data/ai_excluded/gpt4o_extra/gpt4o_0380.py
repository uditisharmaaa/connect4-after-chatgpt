import random
import os

# Constants for the game
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    print("  " + "   ".join(chr(65 + i) for i in range(COLUMNS)))
    for row in board:
        print("+---" * COLUMNS + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * COLUMNS + "+")

def is_valid_input(column):
    return len(column) == 1 and column.isalpha() and 'A' <= column < chr(65 + COLUMNS)

def is_valid_move(board, column):
    col_index = ord(column) - 65
    return board[0][col_index] == " "

def place_checker(board, column, checker):
    col_index = ord(column) - 65
    for row in reversed(board):
        if row[col_index] == " ":
            row[col_index] = checker
            break

def check_winner(board, checker):
    # Check horizontal, vertical, and both diagonal directions
    for row in range(ROWS):
        for col in range(COLUMNS):
            if col <= COLUMNS - 4 and all(board[row][col+k] == checker for k in range(4)):
                return True
            if row <= ROWS - 4 and all(board[row+k][col] == checker for k in range(4)):
                return True
            if col <= COLUMNS - 4 and row <= ROWS - 4 and all(board[row+k][col+k] == checker for k in range(4)):
                return True
            if col <= COLUMNS - 4 and row >= 3 and all(board[row-k][col+k] == checker for k in range(4)):
                return True
    return False

def is_draw(board):
    return all(board[0][col] != " " for col in range(COLUMNS))

def connect4():
    board = create_board()
    starting_player = random.randint(0, PLAYERS - 1)
    current_player = starting_player
    game_over = False
    
    print_board(board)
    
    while not game_over:
        print(f"Player {CHECKERS[current_player]}, please enter a column:")
        column = input().strip().upper()
        
        if not is_valid_input(column):
            print("Invalid input, please enter a valid column letter.")
            continue
        
        if not is_valid_move(board, column):
            print("Column is full or invalid, choose another column.")
            continue
        
        place_checker(board, column, CHECKERS[current_player])
        print_board(board)
        
        if check_winner(board, CHECKERS[current_player]):
            print(f"Player {CHECKERS[current_player]} won!")
            game_over = True
        elif is_draw(board):
            print("The game is a draw!")
            game_over = True
        else:
            current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    connect4()
