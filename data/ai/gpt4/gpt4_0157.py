import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
TOKENS = ["X", "O", "V", "H", "M"]

# Initialize board
def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

# Print the board
def print_board(board):
    os.system('clear')
    print("  " + "   ".join([chr(65 + i) for i in range(COLS)]))
    print("+---" * COLS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLS + "+")

# Check for valid input
def is_valid_column(col, cols, board):
    return 0 <= col < cols and board[0][col] == " "

# Drop checker into column
def drop_checker(board, col, token):
    for row in reversed(board):
        if row[col] == " ":
            row[col] = token
            return True
    return False

# Check for a win
def check_win(board, rows, cols, token):
    # Check horizontal
    for r in range(rows):
        for c in range(cols - 3):
            if all(board[r][c + i] == token for i in range(4)):
                return True
    # Check vertical
    for r in range(rows - 3):
        for c in range(cols):
            if all(board[r + i][c] == token for i in range(4)):
                return True
    # Check diagonal (bottom-left to top-right)
    for r in range(rows - 3):
        for c in range(cols - 3):
            if all(board[r + i][c + i] == token for i in range(4)):
                return True
    # Check diagonal (top-left to bottom-right)
    for r in range(3, rows):
        for c in range(cols - 3):
            if all(board[r - i][c + i] == token for i in range(4)):
                return True
    return False

# Check for draw
def is_draw(board):
    return all(cell != " " for row in board for cell in row)

# Main game
def main():
    # Setup
    board = create_board(ROWS, COLS)
    tokens = TOKENS[:PLAYERS]
    turn = random.randint(0, PLAYERS - 1)
    print_board(board)
    
    while True:
        # Get input
        token = tokens[turn]
        print(f"Player {token}, please enter a column:")
        col_input = input().strip().upper()
        if len(col_input) != 1 or not col_input.isalpha():
            print("Invalid input. Enter a valid column letter.")
            continue
        col = ord(col_input) - 65
        if not is_valid_column(col, COLS, board):
            print("Invalid or full column. Try again.")
            continue
        # Drop checker and update board
        drop_checker(board, col, token)
        print_board(board)
        
        # Check for win/draw
        if check_win(board, ROWS, COLS, token):
            print(f"Player {token} won!")
            break
        if is_draw(board):
            print("It's a draw!")
            break
        
        # Switch turn
        turn = (turn + 1) % PLAYERS

if __name__ == "__main__":
    main()
