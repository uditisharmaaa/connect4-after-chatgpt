import os
import random

# Constants for board dimensions and player symbols
ROWS = 6
COLS = 7
PLAYERS = ["X", "O", "V", "H", "M"]  # Players' symbols for up to 5 players

def create_board():
    """Creates a board initialized with whitespaces."""
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Prints the current state of the board."""
    os.system('clear')  # Clear the screen for a clean display
    print("  " + "   ".join(chr(i) for i in range(65, 65 + COLS)))  # Column labels A, B, C, ...
    print("+---" + "---+" * COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" + "---+" * COLS)

def get_valid_input(current_player):
    """Asks for valid column input and returns the column index."""
    while True:
        user_input = input(f"Player {current_player}, please enter a column: ").upper()  # Ensure uppercase
        if len(user_input) != 1 or user_input < 'A' or user_input >= chr(65 + COLS):
            print("Invalid input. Please enter a letter corresponding to a column (A-G).")
            continue
        col_index = ord(user_input) - 65
        if board[0][col_index] != " ":  # Check if the column is full
            print("This column is full. Please choose another column.")
        else:
            return col_index

def place_checker(board, col_index, player_symbol):
    """Places the player's checker in the specified column."""
    for row in reversed(board):  # Start from the bottom row
        if row[col_index] == " ":
            row[col_index] = player_symbol
            return

def check_winner(board, player_symbol):
    """Checks if the specified player has won."""
    # Check horizontal, vertical, and diagonal (both directions)
    for r in range(ROWS):
        for c in range(COLS - 3):
            if all(board[r][c + i] == player_symbol for i in range(4)):
                return True

    for c in range(COLS):
        for r in range(ROWS - 3):
            if all(board[r + i][c] == player_symbol for i in range(4)):
                return True

    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if all(board[r + i][c + i] == player_symbol for i in range(4)):  # Diagonal down-right
                return True
    
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if all(board[r - i][c + i] == player_symbol for i in range(4)):  # Diagonal down-left
                return True

    return False

def is_draw(board):
    """Checks if the board is full and no player has won."""
    return all(board[0][c] != " " for c in range(COLS)) and not any(check_winner(board, player) for player in PLAYERS[:num_players])

# Main game logic
board = create_board()
num_players = 2  # Set number of players (2 players)
current_player_index = random.randint(0, num_players - 1)  # Randomly determine the first player

# Main game loop
while True:
    print_board(board)
    current_player = PLAYERS[current_player_index]

    col_index = get_valid_input(current_player)
    place_checker(board, col_index, current_player)

    if check_winner(board, current_player):
        print_board(board)
        print(f"Player {current_player} won!")
        break

    if is_draw(board):
        print_board(board)
        print("The game is a draw!")
        break

    # Switch to the next player
    current_player_index = (current_player_index + 1) % num_players
