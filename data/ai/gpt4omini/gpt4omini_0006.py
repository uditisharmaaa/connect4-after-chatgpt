import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O', 'V', 'H', 'M']  # Up to 5 players

def create_board():
    """Create and return a new game board."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current game board."""
    os.system('clear')  # Clear the console
    column_labels = "  " + "   ".join(chr(65 + i) for i in range(COLS))  # A-G
    print(column_labels)
    print("+" + "---+" * COLS)
    
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)

def get_valid_input(player):
    """Get valid column input from the current player."""
    while True:
        column = input(f"Player {player}, please enter a column (A-G): ").strip().upper()
        if len(column) == 1 and 'A' <= column <= 'G':
            col_index = ord(column) - 65
            if board[0][col_index] == ' ':
                return col_index
            else:
                print("Column is full. Try another one!")
        else:
            print("Invalid input. Please enter a letter (A-G).")

def place_checker(board, col, player):
    """Place the player's checker in the specified column."""
    for row in reversed(range(ROWS)):
        if board[row][col] == ' ':
            board[row][col] = player
            return True
    return False

def check_win(board, player):
    """Check if the specified player has won the game."""
    # Check horizontal, vertical, and diagonal
    for row in range(ROWS):
        for col in range(COLS):
            if (check_direction(board, row, col, 0, 1, player) or  # Horizontal
                check_direction(board, row, col, 1, 0, player) or  # Vertical
                check_direction(board, row, col, 1, 1, player) or  # Diagonal \
                check_direction(board, row, col, 1, -1, player)):  # Diagonal /
                return True
    return False

def check_direction(board, row, col, d_row, d_col, player):
    """Check for 4 in a row in the specified direction."""
    count = 0
    for i in range(4):
        r = row + i * d_row
        c = col + i * d_col
        if 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == player:
            count += 1
        else:
            break
    return count == 4

def check_draw(board):
    """Check if the game is a draw (board is full)."""
    for row in board[0]:
        if row == ' ':
            return False
    return True

# Initialize the game
board = create_board()
current_player = random.choice(PLAYERS)
print_board(board)

while True:
    col_index = get_valid_input(current_player)
    place_checker(board, col_index, current_player)
    print_board(board)

    if check_win(board, current_player):
        print(f"Player {current_player} won!")
        break

    if check_draw(board):
        print("The game is a draw!")
        break

    current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % len(PLAYERS)]
