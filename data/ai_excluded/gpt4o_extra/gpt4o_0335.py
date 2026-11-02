import os
import random

# Constants for the game dimensions and number of players
ROWS = 6
COLUMNS = 7
PLAYERS = 2

# Checker symbols for players
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def clear_screen():
    os.system('clear')

def create_board():
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    col_labels = ' '.join([chr(ord('A') + i) for i in range(COLUMNS)])
    print(f"  {col_labels}")
    print("+---" * COLUMNS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

def is_valid_input(input_str):
    return input_str.isalpha() and len(input_str) == 1 and 'A' <= input_str <= chr(ord('A') + COLUMNS - 1)

def get_next_open_row(board, col):
    for r in range(ROWS):
        if board[r][col] == ' ':
            return r
    return None

def place_checker(board, row, col, checker):
    board[row][col] = checker

def check_for_win(board, checker):
    # Check horizontal locations for win
    for c in range(COLUMNS - 3):
        for r in range(ROWS):
            if all(board[r][c+i] == checker for i in range(4)):
                return True

    # Check vertical locations for win
    for c in range(COLUMNS):
        for r in range(ROWS - 3):
            if all(board[r+i][c] == checker for i in range(4)):
                return True

    # Check positive diagonal locations for win
    for c in range(COLUMNS - 3):
        for r in range(ROWS - 3):
            if all(board[r+i][c+i] == checker for i in range(4)):
                return True

    # Check negative diagonal locations for win
    for c in range(COLUMNS - 3):
        for r in range(3, ROWS):
            if all(board[r-i][c+i] == checker for i in range(4)):
                return True

    return False

def is_board_full(board):
    return all(board[r][c] != ' ' for r in range(ROWS) for c in range(COLUMNS))

def main():
    board = create_board()
    print_board(board)
    
    current_player = random.randint(0, PLAYERS - 1)
    
    while True:
        checker = CHECKERS[current_player]
        print(f"Player {checker}, please enter a column:")
        
        while True:
            col_input = input().strip().upper()
            if not is_valid_input(col_input):
                print("Invalid input. Please enter a valid column letter.")
                continue
            
            col_index = ord(col_input) - ord('A')
            row_index = get_next_open_row(board, col_index)
            if row_index is None:
                print("Column full. Please choose another column.")
                continue
            
            break
        
        place_checker(board, row_index, col_index, checker)
        print_board(board)
        
        if check_for_win(board, checker):
            print(f"Player {checker} won!")
            break
        
        if is_board_full(board):
            print("The game is a draw.")
            break
        
        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
