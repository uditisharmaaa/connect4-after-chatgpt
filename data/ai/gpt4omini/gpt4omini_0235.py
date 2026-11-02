import os
import random

# Constants for the game dimensions and player checkers
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
CHECKERS = ["X", "O", "V", "H", "M"]

# Function to create an empty game board
def create_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

# Function to print the game board
def print_board(board):
    os.system('clear')  # Clear the console
    print("  " + "   ".join(chr(65 + i) for i in range(COLUMNS)))  # Column headers
    print("+---" + "---+" * COLUMNS)  # Top border
    for row in board:
        print("| " + " | ".join(row) + " |")  # Row representation
        print("+---" + "---+" * COLUMNS)  # Row border
    print()

# Function to check for a winning condition
def check_winner(board, player):
    # Check horizontal, vertical, and diagonal win conditions
    for r in range(ROWS):
        for c in range(COLUMNS):
            if board[r][c] == player:
                # Check horizontal
                if c + 3 < COLUMNS and all(board[r][c + i] == player for i in range(4)):
                    return True
                # Check vertical
                if r + 3 < ROWS and all(board[r + i][c] == player for i in range(4)):
                    return True
                # Check diagonal (down-right)
                if r + 3 < ROWS and c + 3 < COLUMNS and all(board[r + i][c + i] == player for i in range(4)):
                    return True
                # Check diagonal (down-left)
                if r + 3 < ROWS and c - 3 >= 0 and all(board[r + i][c - i] == player for i in range(4)):
                    return True
    return False

# Function to check for a draw condition
def check_draw(board):
    return all(board[0][c] != " " for c in range(COLUMNS))

# Function to place a checker in the specified column
def place_checker(board, column, checker):
    for r in range(ROWS - 1, -1, -1):  # Start from the bottom row
        if board[r][column] == " ":
            board[r][column] = checker
            return True
    return False  # Column is full

# Function to get valid column input from the player
def get_column_input(player):
    while True:
        col_input = input(f"Player {player}, please enter a column (A-G): ").upper()
        if len(col_input) == 1 and 'A' <= col_input <= 'G':
            column = ord(col_input) - 65  # Convert letter to column index
            return column
        else:
            print("Invalid input. Please enter a letter from A to G.")

# Main game loop
def play_connect_4():
    board = create_board()
    players = CHECKERS[:2]  # Only two players as per submission requirements
    current_player = random.choice(players)

    print_board(board)

    while True:
        col = get_column_input(current_player)
        
        if place_checker(board, col, current_player):
            print_board(board)

            if check_winner(board, current_player):
                print(f"Player {current_player} won!")
                break
            
            if check_draw(board):
                print("The game is a draw!")
                break
            
            # Switch to the next player
            current_player = players[(players.index(current_player) + 1) % len(players)]
        else:
            print("Column is full. Try again.")

# Start the game
if __name__ == "__main__":
    play_connect_4()
