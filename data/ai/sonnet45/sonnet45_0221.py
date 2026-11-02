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
        print("+" + "---+" * COLS)
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
    print("+" + "---+" * COLS)

def is_valid_column(col_letter, board):
    if len(col_letter) != 1 or not col_letter.isalpha() or not col_letter.isupper():
        return False
    col_index = ord(col_letter) - 65
    if col_index < 0 or col_index >= COLS:
        return False
    return board[0][col_index] == " "

def place_checker(board, col_letter, checker):
    col_index = ord(col_letter) - 65
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = checker
            return row, col_index
    return None, None

def check_win(board, row, col, checker):
    # Horizontal
    count = 0
    for c in range(COLS):
        if board[row][c] == checker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
    
    # Vertical
    count = 0
    for r in range(ROWS):
        if board[r][col] == checker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
    
    # Diagonal (bottom-left to top-right)
    count = 0
    start_r = row - min(row, col)
    start_c = col - min(row, col)
    while start_r < ROWS and start_c < COLS:
        if board[start_r][start_c] == checker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
        start_r += 1
        start_c += 1
    
    # Diagonal (top-left to bottom-right)
    count = 0
    start_r = row + min(ROWS - 1 - row, col)
    start_c = col - min(ROWS - 1 - row, col)
    while start_r >= 0 and start_c < COLS:
        if board[start_r][start_c] == checker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
        start_r -= 1
        start_c += 1
    
    return False

def is_board_full(board):
    return all(board[0][c] != " " for c in range(COLS))

def main():
    board = create_board()
    players = CHECKERS[:NUM_PLAYERS]
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    print_board(board)
    
    while True:
        checker = players[current_player]
        col_letter = input(f"Player {checker}, please enter a column: ")
        
        if not is_valid_column(col_letter, board):
            print("Invalid input. Try again.")
            continue
        
        row, col = place_checker(board, col_letter, checker)
        print_board(board)
        
        if check_win(board, row, col, checker):
            print(f"Player {checker} won!")
            break
        
        if is_board_full(board):
            print("It's a draw!")
            break
        
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
