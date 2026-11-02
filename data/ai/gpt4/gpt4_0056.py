import os
import random

# Constants for the game configuration
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]

# Function to create the game board
def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

# Function to print the game board
def print_board(board):
    os.system('clear')  # Clear screen
    col_labels = "   ".join(chr(65 + i) for i in range(len(board[0])))
    print(f"  {col_labels}")
    print("+---" * len(board[0]) + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * len(board[0]) + "+")

# Function to validate user input
def valid_input(inp, board):
    if len(inp) != 1 or not inp.isalpha():
        return False
    col = ord(inp.upper()) - 65
    return 0 <= col < len(board[0]) and board[0][col] == " "

# Function to place a checker in the correct position
def place_checker(board, col, symbol):
    for row in reversed(board):
        if row[col] == " ":
            row[col] = symbol
            break

# Function to check for win conditions
def check_winner(board, symbol):
    rows, cols = len(board), len(board[0])

    # Check horizontal win
    for r in range(rows):
        for c in range(cols - 3):
            if all(board[r][c + i] == symbol for i in range(4)):
                return True

    # Check vertical win
    for r in range(rows - 3):
        for c in range(cols):
            if all(board[r + i][c] == symbol for i in range(4)):
                return True

    # Check diagonal (\ direction) win
    for r in range(rows - 3):
        for c in range(cols - 3):
            if all(board[r + i][c + i] == symbol for i in range(4)):
                return True

    # Check diagonal (/ direction) win
    for r in range(3, rows):
        for c in range(cols - 3):
            if all(board[r - i][c + i] == symbol for i in range(4)):
                return True

    return False

# Function to check if the board is full (draw condition)
def check_draw(board):
    return all(board[0][c] != " " for c in range(len(board[0])))

# Main function to play the game
def play_game():
    # Initialize game
    board = create_board(ROWS, COLUMNS)
    num_players = 2  # You can modify this for more players
    players = PLAYER_SYMBOLS[:num_players]
    current_player = random.choice(players)  # Randomly select the first player

    # Game loop
    while True:
        print_board(board)
        print(f"Player {current_player}'s turn. Please enter a column:")
        while True:
            choice = input().strip().upper()
            if valid_input(choice, board):
                col = ord(choice) - 65
                break
            else:
                print("Invalid input. Please enter a valid column:")

        # Place the checker and check win/draw conditions
        place_checker(board, col, current_player)
        if check_winner(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break
        if check_draw(board):
            print_board(board)
            print("The game is a draw!")
            break

        # Switch to the next player
        current_player = players[(players.index(current_player) + 1) % num_players]

if __name__ == "__main__":
    play_game()
