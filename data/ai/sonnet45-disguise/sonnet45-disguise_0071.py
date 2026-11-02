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
        print("|", end="")
        for j in range(COLS):
            print(" " + board[i][j] + " |", end="")
        print()
    print("+---" * COLS + "+")

def get_column_input(player):
    col = input("Player " + player + ", please enter a column: ")
    return col

def is_valid_input(col, board):
    if len(col) != 1:
        return False
    
    if not col.isalpha():
        return False
    
    col = col.upper()
    col_num = ord(col) - 65
    
    if col_num < 0 or col_num >= COLS:
        return False
    
    if board[0][col_num] != " ":
        return False
    
    return True

def place_checker(board, col, checker):
    col = col.upper()
    col_num = ord(col) - 65
    
    for i in range(ROWS - 1, -1, -1):
        if board[i][col_num] == " ":
            board[i][col_num] = checker
            return i, col_num
    
    return -1, -1

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
    start_r = row
    start_c = col
    while start_r < ROWS - 1 and start_c > 0:
        start_r += 1
        start_c -= 1
    
    r = start_r
    c = start_c
    while r >= 0 and c < COLS:
        if board[r][c] == checker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
        r -= 1
        c += 1
    
    # Check diagonal (top-left to bottom-right)
    count = 0
    start_r = row
    start_c = col
    while start_r > 0 and start_c > 0:
        start_r -= 1
        start_c -= 1
    
    r = start_r
    c = start_c
    while r < ROWS and c < COLS:
        if board[r][c] == checker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
        r += 1
        c += 1
    
    return False

def check_draw(board):
    for i in range(COLS):
        if board[0][i] == " ":
            return False
    return True

def main():
    board = create_board()
    players = []
    for i in range(NUM_PLAYERS):
        players.append(CHECKERS[i])
    
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)
    
    print_board(board)
    
    game_over = False
    
    while not game_over:
        current_player = players[current_player_idx]
        
        valid = False
        while not valid:
            col = get_column_input(current_player)
            if is_valid_input(col, board):
                valid = True
            else:
                print("Invalid input! Try again.")
        
        row, col_num = place_checker(board, col, current_player)
        
        print_board(board)
        
        if check_win(board, row, col_num, current_player):
            print("Player " + current_player + " won!")
            game_over = True
        elif check_draw(board):
            print("It's a draw!")
            game_over = True
        else:
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
