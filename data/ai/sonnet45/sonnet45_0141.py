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
    
    # Print board
    for row in board:
        print("+---" * COLS + "+")
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
    print("+---" * COLS + "+")

def is_valid_move(board, col):
    if col < 0 or col >= COLS:
        return False
    return board[0][col] == " "

def place_checker(board, col, checker):
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row
    return -1

def check_win(board, row, col, checker):
    # Check horizontal
    for c in range(COLS - 3):
        if all(board[row][c + i] == checker for i in range(4)):
            return True
    
    # Check vertical
    for r in range(ROWS - 3):
        if all(board[r + i][col] == checker for i in range(4)):
            return True
    
    # Check diagonal (down-right)
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if all(board[r + i][c + i] == checker for i in range(4)):
                return True
    
    # Check diagonal (up-right)
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if all(board[r - i][c + i] == checker for i in range(4)):
                return True
    
    return False

def is_draw(board):
    return all(board[0][col] != " " for col in range(COLS))

def get_valid_input(board, player_checker):
    while True:
        print(f"Player {player_checker}, please enter a column: ", end="")
        user_input = input().strip().upper()
        
        if len(user_input) != 1 or not user_input.isalpha():
            continue
        
        col = ord(user_input) - 65
        
        if is_valid_move(board, col):
            return col

def main():
    board = create_board()
    players = [CHECKERS[i] for i in range(NUM_PLAYERS)]
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    print_board(board)
    
    while True:
        checker = players[current_player]
        col = get_valid_input(board, checker)
        row = place_checker(board, col, checker)
        
        print_board(board)
        
        if check_win(board, row, col, checker):
            print(f"Player {checker} won!")
            break
        
        if is_draw(board):
            print("It's a draw!")
            break
        
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
