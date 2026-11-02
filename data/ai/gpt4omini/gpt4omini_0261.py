import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']

# Initialize board
def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

# Print the board
def print_board(board):
    os.system('clear')
    print("  " + "   ".join(chr(65 + c) for c in range(COLS)))
    print("+---" + "---+" * COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" + "---+" * COLS)

# Check if the move is valid
def is_valid_move(board, col):
    return board[0][col] == " "

# Place the checker and return the row it occupies
def place_checker(board, col, symbol):
    for row in reversed(range(ROWS)):
        if board[row][col] == " ":
            board[row][col] = symbol
            return row
    return -1  # Indicates the column is full

# Check for a win
def check_win(board, symbol):
    for r in range(ROWS):
        for c in range(COLS):
            if (c + 3 < COLS and all(board[r][c+i] == symbol for i in range(4))) or \
               (r + 3 < ROWS and all(board[r+i][c] == symbol for i in range(4))) or \
               (r + 3 < ROWS and c + 3 < COLS and all(board[r+i][c+i] == symbol for i in range(4))) or \
               (r - 3 >= 0 and c + 3 < COLS and all(board[r-i][c+i] == symbol for i in range(4))):
                return True
    return False

# Check for a draw
def is_draw(board):
    return all(board[0][c] != " " for c in range(COLS))

# Main game loop
def main():
    board = create_board()
    current_player = random.randint(0, min(len(PLAYER_SYMBOLS) - 1, 1))
    
    while True:
        print_board(board)
        symbol = PLAYER_SYMBOLS[current_player]
        col_input = input(f"Player {symbol}, please enter a column (A-G): ").upper()
        
        if len(col_input) != 1 or col_input < 'A' or col_input > chr(65 + COLS - 1):
            print("Invalid input. Try again.")
            continue

        col = ord(col_input) - 65
        
        if not is_valid_move(board, col):
            print("Column is full. Try again.")
            continue
        
        place_checker(board, col, symbol)

        if check_win(board, symbol):
            print_board(board)
            print(f"Player {symbol} won!")
            break
        
        if is_draw(board):
            print_board(board)
            print("The game is a draw!")
            break
        
        current_player = (current_player + 1) % min(len(PLAYER_SYMBOLS), 5)

if __name__ == "__main__":
    main()
