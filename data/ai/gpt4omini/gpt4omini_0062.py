import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = ["X", "O"]  # Default to 2 players

def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')  # Clear the terminal screen
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))  # Column labels A, B, C, ...
    print("+" + "---+" * COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)

def get_column_index(column):
    if column.isalpha() and len(column) == 1:
        index = ord(column.upper()) - 65  # Convert A-F to 0-5
        if 0 <= index < COLS:
            return index
    return -1

def drop_checker(board, column, player):
    for row in reversed(board):  # Start from the bottom row
        if row[column] == " ":
            row[column] = player
            return True
    return False  # Column is full

def check_win(board, player):
    # Check horizontal
    for row in board:
        for col in range(COLS - 3):
            if all(row[col + i] == player for i in range(4)):
                return True
                
    # Check vertical
    for col in range(COLS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == player for i in range(4)):
                return True

    # Check diagonal (top-left to bottom-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == player for i in range(4)):
                return True

    # Check diagonal (bottom-left to top-right)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i][col + i] == player for i in range(4)):
                return True

    return False

def check_draw(board):
    return all(cell != " " for row in board for cell in row)

def main():
    board = create_board()
    current_player = random.choice(PLAYERS)
    
    print_board(board)
    
    while True:
        print(f"Player {current_player}, please enter a column:")
        column_input = input().strip()
        column = get_column_index(column_input)
        
        if column == -1:
            print("Invalid input, please enter a valid column letter (A-G).")
            continue
            
        if not drop_checker(board, column, current_player):
            print("Column is full, please try another column.")
            continue
            
        print_board(board)
        
        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            break
            
        if check_draw(board):
            print("The game is a draw!")
            break
        
        current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % len(PLAYERS)]

if __name__ == "__main__":
    main()
