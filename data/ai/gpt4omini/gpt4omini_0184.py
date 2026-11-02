import random
import os

# Constants
ROWS = 6
COLUMNS = 7
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']

# Function to create the Connect 4 board
def create_board():
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

# Function to print the game board
def print_board(board):
    os.system('clear')  # Clear the terminal screen
    print("  " + "   ".join(chr(65 + c) for c in range(COLUMNS)))  # Column labels A-G
    print("+" + "---+" * COLUMNS)  # Top border
    for row in board:
        print("| " + " | ".join(row) + " |")  # Row contents
        print("+" + "---+" * COLUMNS)  # Row border

# Function to drop the checker into the selected column
def drop_checker(board, column, checker):
    for row in reversed(board):  # Start from the bottom of the column
        if row[column] == ' ':
            row[column] = checker
            return True
    return False  # If the column is full

# Function to check for a win
def check_win(board, checker):
    # Check horizontal, vertical and diagonal
    for r in range(ROWS):
        for c in range(COLUMNS):
            if board[r][c] == checker:
                # Check horizontal
                if c + 3 < COLUMNS and all(board[r][c + i] == checker for i in range(4)):
                    return True
                # Check vertical
                if r + 3 < ROWS and all(board[r + i][c] == checker for i in range(4)):
                    return True
                # Check diagonal /
                if r + 3 < ROWS and c - 3 >= 0 and all(board[r + i][c - i] == checker for i in range(4)):
                    return True
                # Check diagonal \
                if r + 3 < ROWS and c + 3 < COLUMNS and all(board[r + i][c + i] == checker for i in range(4)):
                    return True
    return False

# Function to check for a draw
def check_draw(board):
    return all(cell != ' ' for row in board for cell in row)

# Function to get a valid column input from a player
def get_column_input():
    while True:
        user_input = input("Please enter a column (A-G): ").upper()
        if len(user_input) == 1 and 'A' <= user_input <= 'G':
            return ord(user_input) - 65  # Convert letter to column index
        print("Invalid input. Please try again.")

# Main game function
def connect_4():
    board = create_board()
    num_players = min(len(PLAYER_SYMBOLS), 5)  # Support up to 5 players
    current_player = random.randint(0, num_players - 1)
    game_over = False

    while not game_over:
        print_board(board)
        print(f"Player {PLAYER_SYMBOLS[current_player]}, it's your turn.")

        column = get_column_input()
        if drop_checker(board, column, PLAYER_SYMBOLS[current_player]):
            if check_win(board, PLAYER_SYMBOLS[current_player]):
                print_board(board)
                print(f"Player {PLAYER_SYMBOLS[current_player]} won!")
                game_over = True
            elif check_draw(board):
                print_board(board)
                print("The game is a draw!")
                game_over = True
            # Switch players
            current_player = (current_player + 1) % num_players
        else:
            print("Column is full, please choose another column.")

if __name__ == "__main__":
    connect_4()
