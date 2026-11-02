import random
import os

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2

# Player symbols
SYMBOLS = ["X", "O", "V", "H", "M"]

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
    for row in board:
        print("+---" * COLS + "+")
        print("|", end="")
        for cell in row:
            print(" " + cell + " |", end="")
        print()
    print("+---" * COLS + "+")

def get_column_input(player_symbol):
    column = input(f"Player {player_symbol}, please enter a column: ")
    return column

def validate_input(board, column):
    if len(column) != 1:
        return False
    if not column.isalpha():
        return False
    if not column.isupper():
        return False
    
    col_num = ord(column) - 65
    if col_num < 0 or col_num >= COLS:
        return False
    
    # Check if column is full
    if board[0][col_num] != " ":
        return False
    
    return True

def place_checker(board, column, symbol):
    col_num = ord(column) - 65
    
    # Find the lowest available row
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_num] == " ":
            board[row][col_num] = symbol
            return row, col_num
    
    return -1, -1

def check_win(board, row, col, symbol):
    # Check horizontal
    count = 0
    for c in range(COLS):
        if board[row][c] == symbol:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
    
    # Check vertical
    count = 0
    for r in range(ROWS):
        if board[r][col] == symbol:
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
        if board[r][c] == symbol:
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
        if board[r][c] == symbol:
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

def main():
    board = create_board()
    
    # Select random starting player
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    print_board(board)
    
    game_over = False
    
    while not game_over:
        symbol = SYMBOLS[current_player]
        
        # Get valid input
        valid = False
        while not valid:
            column = get_column_input(symbol)
            valid = validate_input(board, column)
            if not valid:
                print("Invalid input. Try again.")
        
        # Place checker
        row, col = place_checker(board, column, symbol)
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_win(board, row, col, symbol):
            print(f"Player {symbol} won!")
            game_over = True
        elif check_draw(board):
            print("It's a draw!")
            game_over = True
        else:
            # Next player's turn
            current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
