import random
import os

# Constants
ROWS, COLS = 6, 7
NUM_PLAYERS = 2
PLAYER_TOKENS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]
COLUMN_LABELS = [chr(i) for i in range(65, 65 + COLS)]

# Initialize board
def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

# Print board
def print_board(board):
    os.system('clear')  # Clear the screen
    print("  " + "   ".join(COLUMN_LABELS))
    print("+---" * COLS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLS + "+")

# Validate column
def validate_column(col, board):
    if col not in COLUMN_LABELS:
        return False
    col_index = COLUMN_LABELS.index(col)
    return board[0][col_index] == " "

# Place checker
def place_checker(player, col, board):
    col_index = COLUMN_LABELS.index(col)
    for row in range(ROWS-1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = PLAYER_TOKENS[player]
            return row, col_index

# Check win conditions
def check_win(row, col, board, token):
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for dr, dc in directions:
        count = 1
        for i in [-1, 1]:
            r, c = row, col
            while 0 <= r+dr*i < ROWS and 0 <= c+dc*i < COLS and board[r+dr*i][c+dc*i] == token:
                count += 1
                r, c = r+dr*i, c+dc*i
        if count >= 4:
            return True
    return False

# Main game loop
def main():
    board = create_board()
    print_board(board)
    current_player = random.randint(0, NUM_PLAYERS - 1)
    moves = 0
    
    while moves < ROWS * COLS:
        print(f"Player {PLAYER_TOKENS[current_player]}, please enter a column:")
        col = input().strip().upper()
        if not validate_column(col, board):
            print("Invalid move, try again!")
            continue
        row, col_index = place_checker(current_player, col, board)
        print_board(board)
        if check_win(row, col_index, board, PLAYER_TOKENS[current_player]):
            print(f"Player {PLAYER_TOKENS[current_player]} won!")
            return
        current_player = (current_player + 1) % NUM_PLAYERS
        moves += 1
    
    print("It's a draw!")

if __name__ == "__main__":
    main()
