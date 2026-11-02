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
    # Print column letters
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

def drop_checker(board, col, checker):
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

def get_valid_input(board):
    while True:
        user_input = input().strip()
        if len(user_input) != 1 or not user_input.isalpha():
            print("Invalid input. Please enter a single letter:")
            continue
        
        user_input = user_input.upper()
        col = ord(user_input) - 65
        
        if col < 0 or col >= COLS:
            print(f"Invalid column. Please enter a letter between A and {chr(64 + COLS)}:")
            continue
        
        if board[0][col] != " ":
            print("Column is full. Please enter another column:")
            continue
        
        return col

def main():
    board = create_board()
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    print_board(board)
    
    while True:
        checker = CHECKERS[current_player]
        print(f"Player {checker}, please enter a column:")
        
        col = get_valid_input(board)
        drop_checker(board, col, checker)
        print_board(board)
        
        if check_win(board, checker):
            print(f"Player {checker} won!")
            break
        
        if check_draw(board):
            print("The game is a draw!")
            break
        
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
