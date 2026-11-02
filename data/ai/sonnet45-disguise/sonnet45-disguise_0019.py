import random
import os

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board():
    board = []
    for i in range(ROWS):
        row = []
        for j in range(COLS):
            row.append(" ")
        board.append(row)
    return board

def print_board(board):
    os.system('clear')
    
    # Print column letters
    print("  ", end="")
    for i in range(COLS):
        print(chr(65 + i) + "   ", end="")
    print()
    
    # Print board
    for row in range(ROWS):
        print("+---" * COLS + "+")
        print("|", end="")
        for col in range(COLS):
            print(" " + board[row][col] + " |", end="")
        print()
    print("+---" * COLS + "+")

def is_valid_move(board, col):
    if col < 0 or col >= COLS:
        return False
    if board[0][col] != " ":
        return False
    return True

def place_checker(board, col, checker):
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row
    return -1

def check_win(board, row, col, checker):
    # Check horizontal
    count = 0
    for c in range(COLS):
        if board[row][c] == checker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
    
    # Check vertical
    count = 0
    for r in range(ROWS):
        if board[r][col] == checker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
    
    # Check diagonal (bottom-left to top-right)
    count = 0
    start_row = row - min(row, col)
    start_col = col - min(row, col)
    r = start_row
    c = start_col
    while r < ROWS and c < COLS:
        if board[r][c] == checker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
        r += 1
        c += 1
    
    # Check diagonal (top-left to bottom-right)
    count = 0
    start_row = row + min(ROWS - 1 - row, col)
    start_col = col - min(ROWS - 1 - row, col)
    r = start_row
    c = start_col
    while r >= 0 and c < COLS:
        if board[r][c] == checker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
        r -= 1
        c += 1
    
    return False

def check_draw(board):
    for col in range(COLS):
        if board[0][col] == " ":
            return False
    return True

def get_player_move(board, player_checker):
    while True:
        print("Player " + player_checker + ", please enter a column: ", end="")
        user_input = input()
        
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        
        if not user_input.isalpha():
            print("Invalid input. Please enter a letter.")
            continue
        
        col_letter = user_input.upper()
        col = ord(col_letter) - 65
        
        if col < 0 or col >= COLS:
            print("Invalid column. Please choose a column between A and " + chr(64 + COLS) + ".")
            continue
        
        if not is_valid_move(board, col):
            print("Column is full. Please choose another column.")
            continue
        
        return col

def main():
    board = create_board()
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    print_board(board)
    
    game_over = False
    while not game_over:
        player_checker = CHECKERS[current_player]
        col = get_player_move(board, player_checker)
        row = place_checker(board, col, player_checker)
        
        print_board(board)
        
        if check_win(board, row, col, player_checker):
            print("Player " + player_checker + " won!")
            game_over = True
        elif check_draw(board):
            print("The game is a draw!")
            game_over = True
        else:
            current_player = (current_player + 1) % NUM_PLAYERS

main()
