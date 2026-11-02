import os
import random

# Constants for the game
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]  # Symbols for up to 5 players
NUM_PLAYERS = 2  # Number of players (can be set to 2-5)
WIN_CONDITION = 4  # Number of checkers in a row to win

# Function to initialize the board
def create_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]

# Function to print the board
def print_board(board):
    os.system('clear')  # Clear the terminal screen
    columns_labels = "  " + "   ".join(chr(65 + i) for i in range(len(board[0])))  # A, B, C ...
    print(columns_labels)
    print("+" + "---+" * len(board[0]))
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * len(board[0]))

# Function to check if a column input is valid
def is_valid_column(column, board):
    if not column.isalpha():  # Must be a letter
        return False
    index = ord(column.upper()) - 65  # Convert column letter to index
    if index < 0 or index >= len(board[0]):  # Check if within bounds
        return False
    if board[0][index] != " ":  # Check if column is not full
        return False
    return True

# Function to place a checker in the proper row of the given column
def drop_checker(board, column, symbol):
    col_index = ord(column.upper()) - 65
    for row in range(len(board) - 1, -1, -1):  # Start from bottom row
        if board[row][col_index] == " ":
            board[row][col_index] = symbol
            return row, col_index  # Return the position of the placed checker

# Check for a win
def check_win(board, row, col, symbol):
    directions = [
        (0, 1),  # Horizontal
        (1, 0),  # Vertical
        (1, 1),  # Diagonal \
        (1, -1), # Diagonal /
    ]
    for dr, dc in directions:
        count = 1
        # Check in the positive direction
        r, c = row + dr, col + dc
        while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == symbol:
            count += 1
            r += dr
            c += dc
        # Check in the negative direction
        r, c = row - dr, col - dc
        while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == symbol:
            count += 1
            r -= dr
            c -= dc
        # Check if there's a win
        if count >= WIN_CONDITION:
            return True
    return False

# Check for a draw
def check_draw(board):
    for row in board:
        if " " in row:
            return False  # If any empty space exists, it's not a draw
    return True

# Main function to play the game
def play_game():
    # Initialize the board
    board = create_board(ROWS, COLUMNS)
    print_board(board)

    # Select first player randomly
    current_player = random.randint(0, NUM_PLAYERS - 1)
    print(f"Player {PLAYER_SYMBOLS[current_player]} will start!")
    
    while True:
        # Get the current player's turn
        print_board(board)
        print(f"Player {PLAYER_SYMBOLS[current_player]}, please enter a column: ")
        column = input().strip().upper()
        
        # Validate input
        while not is_valid_column(column, board):
            print(f"Invalid input. Player {PLAYER_SYMBOLS[current_player]}, please try again: ")
            column = input().strip().upper()

        # Place the checker
        row, col = drop_checker(board, column, PLAYER_SYMBOLS[current_player])

        # Check for a win or draw
        if check_win(board, row, col, PLAYER_SYMBOLS[current_player]):
            print_board(board)
            print(f"Player {PLAYER_SYMBOLS[current_player]} won!")
            break
        elif check_draw(board):
            print_board(board)
            print("It's a draw!")
            break
        
        # Switch to the next player
        current_player = (current_player + 1) % NUM_PLAYERS

# Run the game
if __name__ == "__main__":
    play_game()
