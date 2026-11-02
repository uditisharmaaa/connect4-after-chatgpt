import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')  # Clears the terminal screen
    print("  " + "   ".join("ABCDEFG"[i] for i in range(COLS)))
    print("+" + "---+" * COLS)
    for row in board:
        print("|" + "|".join(row) + "|")
        print("+" + "---+" * COLS)

def is_valid_input(col_input):
    if len(col_input) != 1:
        return False
    col = ord(col_input) - ord('A')
    return 0 <= col < COLS

def place_checker(board, col, checker):
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = checker
            return True
    return False

def check_win(board, checker):
    # Check Horizontal, Vertical, Diagonal
    for r in range(ROWS):
        for c in range(COLS):
            if (c <= COLS - 4 and all(board[r][c + d] == checker for d in range(4))) or \
               (r <= ROWS - 4 and all(board[r + d][c] == checker for d in range(4))) or \
               (r <= ROWS - 4 and c <= COLS - 4 and all(board[r + d][c + d] == checker for d in range(4))) or \
               (r <= ROWS - 4 and c >= 3 and all(board[r + d][c - d] == checker for d in range(4))):
                return True
    return False

def is_draw(board):
    return all(cell != ' ' for row in board for cell in row)

def main():
    board = create_board()
    current_player = random.choice(PLAYERS)
    
    print_board(board)
    
    while True:
        print(f"Player {current_player}, please enter a column:")
        col_input = input().upper()
        
        if not is_valid_input(col_input):
            print("Invalid input. Try again.")
            continue
            
        col = ord(col_input) - ord('A')
        
        if not place_checker(board, col, current_player):
            print("Column is full. Try another column.")
            continue
            
        print_board(board)
        
        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            break
        
        if is_draw(board):
            print("The game is a draw.")
            break
        
        current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % len(PLAYERS)]

if __name__ == "__main__":
    main()
