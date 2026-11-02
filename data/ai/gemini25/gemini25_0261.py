import os
import random

# --- Constants ---
NUM_ROWS = 6
NUM_COLS = 7  # Max 26 columns supported by labels
NUM_PLAYERS = 2  # Between 2 and 5 players
WIN_CONDITION = 4
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]

# --- Global Variables ---
board = []
current_player_index = 0

# --- Helper Functions ---

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')

def create_board():
    """Initializes a new Connect 4 board with empty spaces."""
    global board
    board = [[" " for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]

def print_board():
    """Prints the current state of the Connect 4 board."""
    clear_screen()

    # Print column labels
    print("  " + "   ".join([chr(ord('A') + i) for i in range(NUM_COLS)]))
    for r in range(NUM_ROWS):
        print("+---+" * NUM_COLS + "+")
        row_str = "|"
        for c in range(NUM_COLS):
            row_str += f" {board[r][c]} |"
        print(row_str)
    print("+---+" * NUM_COLS + "+")

def get_column_input(player_checker):
    """
    Prompts the current player for a column input and validates it.
    Returns the 0-indexed column number.
    """
    while True:
        try:
            col_char = input(f"Player {player_checker}, please enter a column: ").upper()
            if not col_char.isalpha() or len(col_char) != 1:
                print("Invalid input. Please enter a single letter (A-{}).".format(chr(ord('A') + NUM_COLS - 1)))
                continue

            col_index = ord(col_char) - ord('A')

            if not (0 <= col_index < NUM_COLS):
                print("Invalid column. Please choose a column between A and {}.".format(chr(ord('A') + NUM_COLS - 1)))
            elif board[0][col_index] != " ": # Check if top row of column is full
                print("Column is full. Please choose another column.")
            else:
                return col_index
        except (ValueError, IndexError):
            print("Invalid input. Please enter a single letter (A-{}).".format(chr(ord('A') + NUM_COLS - 1)))

def drop_checker(col, player_checker):
    """
    Drops the player's checker into the specified column.
    Returns True if successful, False if the column is full (though this is checked before calling).
    """
    for r in range(NUM_ROWS - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = player_checker
            return True
    return False # Should not happen if validation is correct

def check_win(player_checker):
    """
    Checks if the current player has won the game.
    Checks horizontally, vertically, and diagonally.
    """
    # Check horizontal
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS - WIN_CONDITION + 1):
            if all(board[r][c + i] == player_checker for i in range(WIN_CONDITION)):
                return True

    # Check vertical
    for c in range(NUM_COLS):
        for r in range(NUM_ROWS - WIN_CONDITION + 1):
            if all(board[r + i][c] == player_checker for i in range(WIN_CONDITION)):
                return True

    # Check diagonal (top-left to bottom-right)
    for r in range(NUM_ROWS - WIN_CONDITION + 1):
        for c in range(NUM_COLS - WIN_CONDITION + 1):
            if all(board[r + i][c + i] == player_checker for i in range(WIN_CONDITION)):
                return True

    # Check diagonal (bottom-left to top-right)
    for r in range(WIN_CONDITION - 1, NUM_ROWS):
        for c in range(NUM_COLS - WIN_CONDITION + 1):
            if all(board[r - i][c + i] == player_checker for i in range(WIN_CONDITION)):
                return True

    return False

def check_draw():
    """Checks if the board is completely full (a draw)."""
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS):
            if board[r][c] == " ":
                return False
    return True

# --- Main Game Logic ---

def main():
    """Main function to run the Connect 4 game."""
    global current_player_index

    create_board()
    current_player_index = random.randint(0, NUM_PLAYERS - 1) # Randomly select first player

    game_over = False
    winner = None

    while not game_over:
        player_checker = PLAYER_CHECKERS[current_player_index]
        print_board()

        col_index = get_column_input(player_checker)

        # Drop checker (validation already ensures it's a valid move)
        drop_checker(col_index, player_checker)

        if check_win(player_checker):
            winner = player_checker
            game_over = True
        elif check_draw():
            game_over = True
        else:
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

    print_board() # Print final board state

    if winner:
        print(f"Player {winner} won!")
    else:
        print("It's a draw!")

if __name__ == "__main__":
    main()
