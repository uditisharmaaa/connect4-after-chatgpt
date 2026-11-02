import os
import random

# Constants
ROWS = 6  # Number of rows
COLUMNS = 7  # Number of columns
MAX_PLAYERS = 5  # Maximum number of players
CHECKERS = ["X", "O", "V", "H", "M"]  # Checker symbols for up to 5 players
PLAYER_COUNT = 2  # Number of players (default for submission)

# Function to create the board
def create_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]

# Function to display the board
def print_board(board):
    os.system('clear')  # Clear the screen (Linux/Unix)
    print("  " + "   ".join(chr(65 + i) for i in range(len(board[0]))))
    print("+" + "---+" * len(board[0]))
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * len(board[0]))

# Function to validate player input
def validate_input(input_char, board):
    if len(input_char) != 1 or input_char < 'A' or input_char > chr(64 + len(board[0])):
        return False
    column = ord(input_char) - 65
    if board[0][column] != " ":
        return False
    return True

# Function to place a checker
def place_checker(board, column, checker):
    for row in reversed(board):  # Start from the bottom-most row
        if row[column] == " ":
            row[column] = checker
            break

# Function to check if a player has won
def check_win(board, checker):
    rows, cols = len(board), len(board[0])
    
    # Check horizontal win
    for r in range(rows):
        for c in range(cols - 3):
            if all(board[r][c+i] == checker for i in range(4)):
                return True
    
    # Check vertical win
    for r in range(rows - 3):
        for c in range(cols):
            if all(board[r+i][c] == checker for i in range(4)):
                return True
    
    # Check diagonal (\) win
    for r in range(rows - 3):
        for c in range(cols - 3):
            if all(board[r+i][c+i] == checker for i in range(4)):
                return True
    
    # Check diagonal (/) win
    for r in range(3, rows):
        for c in range(cols - 3):
            if all(board[r-i][c+i] == checker for i in range(4)):
                return True
    
    return False

# Function to check if the board is full (draw)
def check_draw(board):
    return all(cell != " " for row in board for cell in row)

# Main game function
def play_connect_4():
    # Create the board
    board = create_board(ROWS, COLUMNS)
    # Randomly pick the first player
    current_player = random.randint(0, PLAYER_COUNT - 1)
    players = CHECKERS[:PLAYER_COUNT]
    
    # Game loop
    while True:
        print_board(board)
        print(f"Player {players[current_player]}, it's your turn:")
        
        # Get player input
        while True:
            column_input = input("Please enter a column (A-G): ").strip().upper()
            if validate_input(column_input, board):
                break
            print("Invalid input. Try again!")

        # Place the checker
        column = ord(column_input) - 65
        place_checker(board, column, players[current_player])

        # Check for win
        if check_win(board, players[current_player]):
            print_board(board)
            print(f"Player {players[current_player]} won!")
            break
        
        # Check for draw
        if check_draw(board):
            print_board(board)
            print("The game is a draw!")
            break

        # Switch to next player
        current_player = (current_player + 1) % PLAYER_COUNT

# Run the game
if __name__ == "__main__":
    play_connect_4()
