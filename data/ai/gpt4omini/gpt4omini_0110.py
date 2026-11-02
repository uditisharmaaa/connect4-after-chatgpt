import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O']  # Expand this for additional players (e.g., ['X', 'O', 'V', 'H', 'M'])

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))
    print("+---" + "---+" * (COLS - 1) + "---+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" + "---+" * (COLS - 1) + "---+")

def is_valid_input(col):
    if len(col) != 1 or not col.isalpha():
        return False
    col_index = ord(col.upper()) - 65
    return 0 <= col_index < COLS

def drop_checker(board, col, checker):
    col_index = ord(col.upper()) - 65
    for row in reversed(range(ROWS)):
        if board[row][col_index] == ' ':
            board[row][col_index] = checker
            return True
    return False

def check_winner(board, checker):
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True
    # Check vertical
    for col in range(COLS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == checker for i in range(4)):
                return True
    # Check diagonal /
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True
    # Check diagonal \
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True
    return False

def is_draw(board):
    return all(board[0][col] != ' ' for col in range(COLS))

def main():
    board = create_board()
    current_player = random.choice(PLAYERS)
    
    print_board(board)
    
    while True:
        print(f"Player {current_player}, please enter a column (A-G): ")
        col = input().strip()
        
        while not is_valid_input(col):
            print("Invalid input. Please enter a valid column (A-G): ")
            col = input().strip()
        
        if not drop_checker(board, col, current_player):
            print("Column is full! You lose your turn.")
        else:
            print_board(board)
            if check_winner(board, current_player):
                print(f"Player {current_player} won!")
                break
            elif is_draw(board):
                print("The game is a draw!")
                break
            
            current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % len(PLAYERS)]

if __name__ == "__main__":
    main()
