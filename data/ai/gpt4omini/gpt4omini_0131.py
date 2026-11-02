import os
import random

# Constants for the game
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    """Creates a game board initialized with empty spaces."""
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Prints the current game board."""
    os.system('clear')
    print("  " + "   ".join(chr(65 + col) for col in range(COLS)))
    print("+---" + "+---" * (COLS - 1) + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" + "+---" * (COLS - 1) + "+")

def is_valid_input(col, board):
    """Checks if the column selected is valid."""
    return col.isalpha() and len(col) == 1 and ord(col.upper()) - 65 < COLS and board[0][ord(col.upper()) - 65] == " "

def get_column_choice(player):
    """Prompt the player to choose a column until a valid input is received."""
    while True:
        col = input(f"Player {player}, please enter a column: ").upper()
        if is_valid_input(col, board):
            return ord(col) - 65
        else:
            print("Invalid input. Please try again.")

def drop_checker(board, col, checker):
    """Drops a checker into the specified column."""
    for row in reversed(board):
        if row[col] == " ":
            row[col] = checker
            return True
    return False

def check_win(board, checker):
    """Checks if the current player has won."""
    # Check horizontal, vertical, and diagonal win conditions
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == checker:
                # Check horizontal
                if col + 3 < COLS and all(board[row][col + i] == checker for i in range(4)):
                    return True
                # Check vertical
                if row + 3 < ROWS and all(board[row + i][col] == checker for i in range(4)):
                    return True
                # Check diagonal (top-left to bottom-right)
                if row + 3 < ROWS and col + 3 < COLS and all(board[row + i][col + i] == checker for i in range(4)):
                    return True
                # Check diagonal (top-right to bottom-left)
                if row + 3 < ROWS and col - 3 >= 0 and all(board[row + i][col - i] == checker for i in range(4)):
                    return True
    return False

def check_draw(board):
    """Checks if the game is a draw."""
    return all(board[0][col] != " " for col in range(COLS))

# Main game loop
board = create_board()
current_player_index = random.randint(0, len(PLAYERS) - 1)

while True:
    print_board(board)
    
    current_player = PLAYERS[current_player_index]
    col = get_column_choice(current_player)

    if drop_checker(board, col, current_player):
        if check_win(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break
        if check_draw(board):
            print_board(board)
            print("The game is a draw!")
            break
        current_player_index = (current_player_index + 1) % len(PLAYERS)
    else:
        print("Column is full or invalid. Please choose a different column.")
