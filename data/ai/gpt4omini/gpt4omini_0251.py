import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = ["X", "O", "V", "H", "M"]  # Up to 5 players

def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')  # Clear terminal (Linux/Unix)
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))  # Column labels (A, B, C, ...)
    print("+" + "---+" * COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)

def is_valid_input(column, board):
    if column < 0 or column >= COLS:
        return False
    return board[0][column] == " "  # Check if the top row of column is empty

def drop_checker(board, column, checker):
    for row in reversed(board):  # Start from the last row and go up
        if row[column] == " ":
            row[column] = checker
            break

def check_winner(board, checker):
    # Check horizontal, vertical, and diagonal
    for r in range(ROWS):
        for c in range(COLS):
            if (c <= COLS - 4 and 
                all(board[r][c + i] == checker for i in range(4))):  # Horizontal
                return True
            if (r <= ROWS - 4 and 
                all(board[r + i][c] == checker for i in range(4))):  # Vertical
                return True
            if (r <= ROWS - 4 and c <= COLS - 4 and 
                all(board[r + i][c + i] == checker for i in range(4))):  # Diagonal \
                return True
            if (r <= ROWS - 4 and c >= 3 and 
                all(board[r + i][c - i] == checker for i in range(4))):  # Diagonal /
                return True
    return False

def check_draw(board):
    return all(board[0][c] != " " for c in range(COLS))

def main():
    board = create_board()
    current_player = random.choice(PLAYERS)
    number_of_players = len(PLAYERS)
    
    while True:
        print_board(board)
        print(f"Player {current_player}, please enter a column (A-{chr(65 + COLS - 1)}):")
        
        # Input handling
        while True:
            user_input = input().strip().upper()
            if len(user_input) != 1 or user_input < 'A' or user_input >= chr(65 + COLS):
                print("Invalid input. Please enter a column letter.")
                continue
            column = ord(user_input) - 65  # Convert letter to column index
            if is_valid_input(column, board):
                drop_checker(board, column, current_player)
                break
            else:
                print("Column is full. Please choose another column.")

        # Check for win
        if check_winner(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break
        
        # Check for draw
        if check_draw(board):
            print_board(board)
            print("The game is a draw!")
            break
        
        # Switch players
        current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % number_of_players]

if __name__ == "__main__":
    main()
