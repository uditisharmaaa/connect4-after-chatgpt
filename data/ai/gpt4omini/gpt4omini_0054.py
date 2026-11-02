import os
import random

# Constants for board dimensions and players
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O', 'V', 'H', 'M']  # Up to 5 players

def create_board():
    """Create a 2D list to represent the board."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the board."""
    os.system('clear')  # Clear the terminal screen
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))
    print("+" + "---+" * COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)

def get_valid_input(player):
    """Get valid column input from the player."""
    while True:
        choice = input(f"Player {player}, please enter a column (A-{chr(65 + COLS - 1)}): ").upper()
        if len(choice) == 1 and 'A' <= choice <= chr(65 + COLS - 1):
            column = ord(choice) - 65
            if board[0][column] == ' ':
                return column
            else:
                print("Column is full! Try a different column.")
        else:
            print("Invalid input! Please enter a valid column.")

def drop_checker(board, column, player):
    """Drop the player's checker in the specified column of the board."""
    for row in reversed(board):
        if row[column] == ' ':
            row[column] = player
            return True
    return False

def check_win(board, player):
    """Check for a win condition for the specified player."""
    # Check horizontal, vertical, and diagonal connections
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == player:
                if (check_direction(board, player, r, c, 1, 0) or  # Horizontal
                    check_direction(board, player, r, c, 0, 1) or  # Vertical
                    check_direction(board, player, r, c, 1, 1) or  # Diagonal /
                    check_direction(board, player, r, c, 1, -1)):  # Diagonal \
                    return True
    return False

def check_direction(board, player, row, col, delta_row, delta_col):
    """Check five cells in a specified direction for a win."""
    count = 0
    for i in range(4):
        new_row = row + i * delta_row
        new_col = col + i * delta_col
        if 0 <= new_row < ROWS and 0 <= new_col < COLS and board[new_row][new_col] == player:
            count += 1
        else:
            break
    return count == 4

def check_draw(board):
    """Check if the board is full and no one has won."""
    return all(board[0][c] != ' ' for c in range(COLS))

# Initialize the game board
board = create_board()

# Randomly choose the first player
current_player_index = random.randint(0, len(PLAYERS) - 1)

# Game loop
while True:
    print_board(board)
    column = get_valid_input(PLAYERS[current_player_index])
    drop_checker(board, column, PLAYERS[current_player_index])

    # Check for win or draw
    if check_win(board, PLAYERS[current_player_index]):
        print_board(board)
        print(f"Player {PLAYERS[current_player_index]} won!")
        break
    if check_draw(board):
        print_board(board)
        print("The game is a draw!")
        break

    # Switch to next player
    current_player_index = (current_player_index + 1) % len(PLAYERS)
