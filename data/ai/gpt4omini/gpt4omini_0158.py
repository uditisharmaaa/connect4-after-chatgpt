import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = ["X", "O"]

def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))
    print("+" + "---+" * COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)

def drop_checker(board, col, checker):
    for row in reversed(board):
        if row[col] == " ":
            row[col] = checker
            return True
    return False

def is_winner(board, checker):
    # Check horizontal
    for row in board:
        for i in range(COLS - 3):
            if row[i] == checker and row[i + 1] == checker and row[i + 2] == checker and row[i + 3] == checker:
                return True

    # Check vertical
    for col in range(COLS):
        for row in range(ROWS - 3):
            if board[row][col] == checker and board[row + 1][col] == checker and \
               board[row + 2][col] == checker and board[row + 3][col] == checker:
                return True

    # Check diagonal (bottom-left to top-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if board[row][col] == checker and board[row + 1][col + 1] == checker and \
               board[row + 2][col + 2] == checker and board[row + 3][col + 3] == checker:
                return True
    
    # Check diagonal (top-left to bottom-right)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if board[row][col] == checker and board[row - 1][col + 1] == checker and \
               board[row - 2][col + 2] == checker and board[row - 3][col + 3] == checker:
                return True

    return False

def is_draw(board):
    for row in board:
        if " " in row:
            return False
    return True

def main():
    board = create_board()
    current_player = random.choice(PLAYERS)
    
    print_board(board)
    
    while True:
        try:
            col_input = input(f"Player {current_player}, please enter a column (A-G): ").upper()
            if col_input < 'A' or col_input > 'G':
                raise ValueError("Invalid column")
            col = ord(col_input) - 65
            
            if not drop_checker(board, col, current_player):
                print("Column is full! Please try again.")
                continue
            
            print_board(board)
            
            if is_winner(board, current_player):
                print(f"Player {current_player} won!")
                break
            
            if is_draw(board):
                print("It's a draw!")
                break
            
            current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % len(PLAYERS)]
        
        except ValueError:
            print("Invalid input! Please enter a letter from A to G.")

if __name__ == "__main__":
    main()
