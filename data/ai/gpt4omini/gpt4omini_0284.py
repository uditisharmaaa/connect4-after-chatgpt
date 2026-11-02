import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = ["X", "O", "V", "H", "M"]

# Initialize the board
def create_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

# Print the game board
def print_board(board):
    os.system('clear')  # Clear the console
    
    # Print column labels
    print("  " + "   ".join(chr(65 + i) for i in range(COLUMNS)))  # A, B, C, ... G
    print("+---" + "---+" * COLUMNS)
    
    # Print rows
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" + "---+" * COLUMNS)

# Check for a win condition
def check_win(board, player):
    # Check horizontal, vertical and diagonal wins
    for r in range(ROWS):
        for c in range(COLUMNS):
            # Horizontal
            if c + 3 < COLUMNS and all(board[r][c + i] == player for i in range(4)):
                return True
            # Vertical
            if r + 3 < ROWS and all(board[r + i][c] == player for i in range(4)):
                return True
            # Diagonal (down-right)
            if r + 3 < ROWS and c + 3 < COLUMNS and all(board[r + i][c + i] == player for i in range(4)):
                return True
            # Diagonal (down-left)
            if r + 3 < ROWS and c - 3 >= 0 and all(board[r + i][c - i] == player for i in range(4)):
                return True
    return False

# Check if the board is full (draw condition)
def check_draw(board):
    return all(board[0][c] != " " for c in range(COLUMNS))

# Place the checker in the board
def place_checker(board, column, player):
    for row in reversed(board):  # Start from the bottom row
        if row[column] == " ":
            row[column] = player
            return True
    return False  # The column is full

# Get a valid column input from the player
def get_valid_column():
    while True:
        column = input(f"Player {current_player}, please enter a column (A-{chr(65 + COLUMNS - 1)}): ").upper()
        if len(column) == 1 and 'A' <= column <= chr(65 + COLUMNS - 1):
            return ord(column) - 65  # Convert to column index
        else:
            print("Invalid input. Please try again.")

# Main game logic
def play_game():
    global current_player
    board = create_board()
    current_player = random.choice(PLAYERS[:2])  # Randomly choose starting player
    game_over = False

    print_board(board)

    while not game_over:
        col = get_valid_column()

        if not place_checker(board, col, current_player):
            print("Column is full. Try again.")
            continue

        print_board(board)
        
        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            game_over = True
        elif check_draw(board):
            print("The game is a draw!")
            game_over = True
        else:
            current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % len(PLAYERS)]

if __name__ == "__main__":
    play_game()
