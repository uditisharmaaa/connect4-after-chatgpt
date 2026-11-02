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
    # Print column headers
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

def get_valid_input(player):
    while True:
        col_input = input(f"Player {player}, please enter a column: ").strip().upper()
        if len(col_input) == 1 and 'A' <= col_input <= chr(64 + COLS):
            return ord(col_input) - 65
        print("Invalid input. Please try again.")

def place_checker(board, col, checker):
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    return False

def check_win(board, checker):
    # Horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True
    
    # Vertical
    for row in range(ROWS - 3):
        for col in range(COLS):
            if all(board[row + i][col] == checker for i in range(4)):
                return True
    
    # Diagonal (down-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True
    
    # Diagonal (down-left)
    for row in range(ROWS - 3):
        for col in range(3, COLS):
            if all(board[row + i][col - i] == checker for i in range(4)):
                return True
    
    return False

def check_draw(board):
    return all(board[0][col] != " " for col in range(COLS))

def main():
    board = create_board()
    players = CHECKERS[:NUM_PLAYERS]
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)
    
    print_board(board)
    
    while True:
        current_checker = players[current_player_idx]
        col = get_valid_input(current_checker)
        
        if not place_checker(board, col, current_checker):
            print("Column is full! You lose your turn.")
        
        print_board(board)
        
        if check_win(board, current_checker):
            print(f"Player {current_checker} won!")
            break
        
        if check_draw(board):
            print("It's a draw!")
            break
        
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
