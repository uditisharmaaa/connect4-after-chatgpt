import os
import random
import string

# --- Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Set to 2 for submission
WIN_CONDITION = 4
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]

# --- Global Variables ---
board = []
players = []
current_player_index = 0

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')

def create_board():
    """Initializes the game board with empty spaces."""
    global board
    board = [[" " for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]

def print_board():
    """Prints the current state of the game board."""
    clear_screen()
    # Print column labels (A, B, C, ...)
    print("  " + "   ".join(string.ascii_uppercase[:NUM_COLS]))
    
    for r in range(NUM_ROWS):
        print("+---" * NUM_COLS + "+")
        row_str = "|"
        for c in range(NUM_COLS):
            row_str += f" {board[r][c]} |"
        print(row_str)
    print("+---" * NUM_COLS + "+")

def get_column_input(prompt):
    """
    Gets validated column input from the player.
    Returns the 0-indexed column number.
    """
    while True:
        col_input = input(prompt).strip().upper()
        if len(col_input) != 1:
            print("Invalid input. Please enter a single letter (e.g., A).")
            continue

        col_char_index = ord(col_input) - ord('A')
        if not (0 <= col_char_index < NUM_COLS):
            print(f"Invalid column. Please enter a letter between A and {string.ascii_uppercase[NUM_COLS-1]}.")
            continue
        
        # Check if column is full
        if board[0][col_char_index] != " ":
            print("That column is full. Please choose another one.")
            continue

        return col_char_index

def drop_checker(col, player_checker):
    """
    Drops the player's checker into the specified column.
    Returns True if the checker was placed, False if the column is full.
    """
    for r in range(NUM_ROWS - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = player_checker
            return True
    return False # Should not be reached due to validation in get_column_input, but good for safety

def check_win(player_checker):
    """
    Checks if the given player has won the game.
    A win occurs if 4 checkers are in a row horizontally, vertically, or diagonally.
    """
    # Check horizontal
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS - WIN_CONDITION + 1):
            if all(board[r][c+i] == player_checker for i in range(WIN_CONDITION)):
                return True

    # Check vertical
    for c in range(NUM_COLS):
        for r in range(NUM_ROWS - WIN_CONDITION + 1):
            if all(board[r+i][c] == player_checker for i in range(WIN_CONDITION)):
                return True

    # Check diagonal (top-left to bottom-right)
    for r in range(NUM_ROWS - WIN_CONDITION + 1):
        for c in range(NUM_COLS - WIN_CONDITION + 1):
            if all(board[r+i][c+i] == player_checker for i in range(WIN_CONDITION)):
                return True

    # Check diagonal (top-right to bottom-left)
    for r in range(NUM_ROWS - WIN_CONDITION + 1):
        for c in range(WIN_CONDITION - 1, NUM_COLS):
            if all(board[r+i][c-i] == player_checker for i in range(WIN_CONDITION)):
                return True
    return False

def check_draw():
    """Checks if the board is completely full (a draw)."""
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS):
            if board[r][c] == " ":
                return False
    return True

def main():
    """Main function to run the Connect 4 game."""
    global players, current_player_index

    # Initialization
    create_board()
    players = PLAYER_CHECKERS[:NUM_PLAYERS]
    current_player_index = random.randint(0, NUM_PLAYERS - 1)

    game_over = False
    winner_checker = None

    while not game_over:
        print_board()
        current_player_checker = players[current_player_index]
        print(f"Player {current_player_checker}, please enter a column:")

        col = get_column_input(f"Player {current_player_checker}, please enter a column: ")
        
        # Drop checker (should always succeed due to validation)
        drop_checker(col, current_player_checker)

        # Check for win
        if check_win(current_player_checker):
            winner_checker = current_player_checker
            game_over = True
        # Check for draw
        elif check_draw():
            game_over = True
        else:
            # Next player's turn
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
    
    # Game over, print final board and result
    print_board()
    if winner_checker:
        print(f"Player {winner_checker} won!")
    else:
        print("The game is a draw!")

if __name__ == "__main__":
    main()
