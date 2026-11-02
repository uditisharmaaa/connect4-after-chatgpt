import random
import os

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    # Print column labels
    print("  ", end="")
    for i in range(COLS):
        print(f" {chr(65 + i)}  ", end="")
    print()
    
    # Print rows
    for row in board:
        print("+---" * COLS + "+")
        print("| ", end="")
        for cell in row:
            print(f"{cell} | ", end="")
        print()
    print("+---" * COLS + "+")

def get_valid_column(board, player):
    while True:
        col_input = input(f"Player {player}, please enter a column: ").strip().upper()
        
        if len(col_input) != 1 or not col_input.isalpha():
            print("Invalid input. Please enter a single letter.")
            continue
        
        col_index = ord(col_input) - 65
        
        if col_index < 0 or col_index >= COLS:
            print(f"Column out of range. Please choose A-{chr(64 + COLS)}.")
            continue
        
        if board[0][col_index] != " ":
            print("Column is full. You lose your turn.")
            return None
        
        return col_index

def place_checker(board, col, checker):
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row
    return -1

def check_win(board, row, col, checker):
    # Horizontal
    for c in range(COLS - 3):
        if all(board[row][c + i] == checker for i in range(4)):
            return True
    
    # Vertical
    for r in range(ROWS - 3):
        if all(board[r + i][col] == checker for i in range(4)):
            return True
    
    # Diagonal (down-right)
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if all(board[r + i][c + i] == checker for i in range(4)):
                return True
    
    # Diagonal (up-right)
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if all(board[r - i][c + i] == checker for i in range(4)):
                return True
    
    return False

def check_draw(board):
    return all(board[0][c] != " " for c in range(COLS))

def main():
    board = create_board()
    players = CHECKERS[:NUM_PLAYERS]
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    print_board(board)
    
    while True:
        current_checker = players[current_player_index]
        col = get_valid_column(board, current_checker)
        
        if col is None:
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            continue
        
        row = place_checker(board, col, current_checker)
        print_board(board)
        
        if check_win(board, row, col, current_checker):
            print(f"Player {current_checker} won!")
            break
        
        if check_draw(board):
            print("It's a draw!")
            break
        
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
