import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O', 'V', 'H', 'M']

# Initialize the board
def initialize_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

# Print the board
def print_board(board):
    os.system('clear')  # Clear the screen
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))  # Column labels
    print("+---" + "---+" * COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" + "---+" * COLS)

# Check if the column is full
def is_column_full(board, col):
    return board[0][col] != ' '

# Drop the checker into the board
def drop_checker(board, col, checker):
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = checker
            return True
    return False

# Check for win
def check_winner(board, checker):
    # Check horizontal, vertical, and diagonal
    for r in range(ROWS):
        for c in range(COLS):
            if (c <= COLS - 4 and all(board[r][c + i] == checker for i in range(4))) or \
               (r <= ROWS - 4 and all(board[r + i][c] == checker for i in range(4))) or \
               (r <= ROWS - 4 and c <= COLS - 4 and all(board[r + i][c + i] == checker for i in range(4))) or \
               (r >= 3 and c <= COLS - 4 and all(board[r - i][c + i] == checker for i in range(4))):
                return True
    return False

# Check for draw
def is_draw(board):
    return all(board[0][c] != ' ' for c in range(COLS))

# Main game loop
def main():
    board = initialize_board()
    current_player = random.choice(PLAYERS[:2])  # Randomly select the first player

    while True:
        print_board(board)
        col_input = input(f"Player {current_player}, please enter a column (A-G): ").upper()
        
        try:
            col = ord(col_input) - 65  # Convert letter to column index
            if col < 0 or col >= COLS:
                raise ValueError("Invalid column. It must be A-G.")
            if is_column_full(board, col):
                print("Column is full, please choose another column.")
                continue
            drop_checker(board, col, current_player)
            
            if check_winner(board, current_player):
                print_board(board)
                print(f"Player {current_player} won!")
                break
            if is_draw(board):
                print_board(board)
                print("The game is a draw!")
                break
            
            current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % len(PLAYERS)]  # Switch player

        except (ValueError, IndexError):
            print("Invalid input, please enter a valid column (A-G)")

if __name__ == "__main__":
    main()
