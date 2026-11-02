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
    # Print column labels
    print("  ", end="")
    for i in range(COLS):
        print(chr(65 + i) + "   ", end="")
    print()
    
    # Print rows
    for i in range(ROWS):
        print("+---" * COLS + "+")
        print("| ", end="")
        for j in range(COLS):
            print(board[i][j] + " | ", end="")
        print()
    print("+---" * COLS + "+")

def is_valid_move(board, col):
    if col < 0 or col >= COLS:
        return False
    if board[0][col] != " ":
        return False
    return True

def place_checker(board, col, checker):
    for i in range(ROWS - 1, -1, -1):
        if board[i][col] == " ":
            board[i][col] = checker
            return i
    return -1

def check_win(board, row, col, checker):
    # Check horizontal
    count = 0
    for j in range(COLS):
        if board[row][j] == checker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
    
    # Check vertical
    count = 0
    for i in range(ROWS):
        if board[i][col] == checker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
    
    # Check diagonal (down-right)
    count = 0
    start_row = row - min(row, col)
    start_col = col - min(row, col)
    i = start_row
    j = start_col
    while i < ROWS and j < COLS:
        if board[i][j] == checker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
        i += 1
        j += 1
    
    # Check diagonal (up-right)
    count = 0
    start_row = row + min(ROWS - 1 - row, col)
    start_col = col - min(ROWS - 1 - row, col)
    i = start_row
    j = start_col
    while i >= 0 and j < COLS:
        if board[i][j] == checker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
        i -= 1
        j += 1
    
    return False

def check_draw(board):
    for j in range(COLS):
        if board[0][j] == " ":
            return False
    return True

def get_player_move(board, player):
    while True:
        print_board(board)
        col_input = input(f"Player {player}, please enter a column: ")
        
        if len(col_input) != 1:
            continue
        
        if not col_input.isalpha():
            continue
        
        col_input = col_input.upper()
        col = ord(col_input) - 65
        
        if col < 0 or col >= COLS:
            continue
        
        if not is_valid_move(board, col):
            continue
        
        return col

def main():
    board = create_board()
    players = []
    for i in range(NUM_PLAYERS):
        players.append(CHECKERS[i])
    
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)
    
    print_board(board)
    
    game_over = False
    while not game_over:
        current_checker = players[current_player_idx]
        col = get_player_move(board, current_checker)
        row = place_checker(board, col, current_checker)
        
        if check_win(board, row, col, current_checker):
            print_board(board)
            print(f"Player {current_checker} won!")
            game_over = True
        elif check_draw(board):
            print_board(board)
            print("The game is a draw!")
            game_over = True
        else:
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

main()
