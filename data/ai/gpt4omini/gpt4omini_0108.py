import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = ["X", "O", "V", "H", "M"]

# Initialize the board
def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

# Print the board
def print_board(board):
    os.system('clear')  # Clear the console
    print("  " + "   ".join([chr(i) for i in range(65, 65 + COLS)]))  # Column labels A-G
    print("+" + "---+" * COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)

# Select the first player randomly
def select_first_player():
    return random.choice(range(len(PLAYERS)))

# Check if the column is valid and available
def is_valid_column(board, col):
    return 0 <= col < COLS and board[0][col] == " "

# Place the checker in the board
def place_checker(board, col, player):
    for row in reversed(range(ROWS)):
        if board[row][col] == " ":
            board[row][col] = player
            return True
    return False  # Column is full

# Check for win conditions
def check_win(board, player):
    # Check horizontal, vertical, and diagonal
    # Horizontal
    for r in range(ROWS):
        for c in range(COLS - 3):
            if all(board[r][c + i] == player for i in range(4)):
                return True

    # Vertical
    for c in range(COLS):
        for r in range(ROWS - 3):
            if all(board[r + i][c] == player for i in range(4)):
                return True

    # Diagonal (top-left to bottom-right)
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if all(board[r + i][c + i] == player for i in range(4)):
                return True

    # Diagonal (top-right to bottom-left)
    for r in range(ROWS - 3):
        for c in range(3, COLS):
            if all(board[r + i][c - i] == player for i in range(4)):
                return True

    return False

# Check for draw
def is_draw(board):
    return all(board[0][c] != " " for c in range(COLS))

# Game loop
def play_game():
    board = create_board()
    current_player_index = select_first_player()
    
    while True:
        print_board(board)
        current_player = PLAYERS[current_player_index]
        col_input = input(f"Player {current_player}, please enter a column: ").strip().upper()

        # Validate input
        if len(col_input) != 1 or not ('A' <= col_input <= 'G'):
            print("Invalid input. Please enter a column letter (A-G).")
            continue

        col = ord(col_input) - 65
        
        if not is_valid_column(board, col):
            print("Column is full or out of bounds. Please choose another column.")
            continue
        
        place_checker(board, col, current_player)

        if check_win(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break

        if is_draw(board):
            print_board(board)
            print("The game is a draw!")
            break

        # Switch player
        current_player_index = (current_player_index + 1) % len(PLAYERS)

# Start the game
if __name__ == "__main__":
    play_game()
