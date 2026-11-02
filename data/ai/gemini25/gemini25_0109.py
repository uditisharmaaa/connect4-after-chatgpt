import os
import random

# --- Constants ---
NUM_ROWS = 6
NUM_COLS = 7  # Max 26 columns
NUM_PLAYERS = 2  # Between 2 and 5 players
CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]
WIN_CONDITION = 4  # Number of checkers to win

# --- Global Board Variable ---
board = []

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')

def create_board():
    """Initializes the game board with empty spaces."""
    global board
    board = [[' ' for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]

def print_board():
    """Prints the current state of the game board."""
    clear_screen()
    # Print column labels
    col_labels = [chr(ord('A') + i) for i in range(NUM_COLS)]
    print("  " + "   ".join(col_labels))

    # Print board rows
    for r in range(NUM_ROWS):
        print("+---" * NUM_COLS + "+")
        row_str = "|"
        for c in range(NUM_COLS):
            row_str += f" {board[r][c]} |"
        print(row_str)
    print("+---" * NUM_COLS + "+")

def get_column_input(player_checker):
    """
    Prompts the current player for a column input and validates it.
    Returns the 0-indexed column number.
    """
    while True:
        try:
            col_char = input(f"Player {player_checker}, please enter a column: ").upper()
            if not (len(col_char) == 1 and 'A' <= col_char <= chr(ord('A') + NUM_COLS - 1)):
                raise ValueError("Invalid column. Please enter a letter between A and " + chr(ord('A') + NUM_COLS - 1))

            col_idx = ord(col_char) - ord('A')

            if board[0][col_idx] != ' ':  # Check if the top of the column is full
                raise ValueError("Column is full. Please choose another column.")

            return col_idx
        except ValueError as e:
            print(f"Error: {e}")

def place_checker(col_idx, player_checker):
    """
    Places the player's checker in the lowest available space in the specified column.
    Returns True if successful, False if the column is full (though this is checked before calling).
    """
    for r in range(NUM_ROWS - 1, -1, -1):
        if board[r][col_idx] == ' ':
            board[r][col_idx] = player_checker
            return True
    return False # Should not be reached due to prior validation

def check_win(player_checker):
    """
    Checks if the current player has achieved a win condition (4 in a row)
    horizontally, vertically, or diagonally.
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

    # Check diagonal (top-right to bottom-left)
    for r in range(NUM_ROWS - WIN_CONDITION + 1):
        for c in range(WIN_CONDITION - 1, NUM_COLS):
            if all(board[r + i][c - i] == player_checker for i in range(WIN_CONDITION)):
                return True

    return False

def check_draw():
    """Checks if the board is completely full (a draw)."""
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS):
            if board[r][c] == ' ':
                return False
    return True

def main():
    create_board()

    # Randomly select the first player
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)

    while True:
        player_checker = CHECKERS[current_player_idx]
        print_board()
        
        col_idx = get_column_input(player_checker)
        place_checker(col_idx, player_checker)

        if check_win(player_checker):
            print_board()
            print(f"Player {player_checker} won!")
            break
        elif check_draw():
            print_board()
            print("It's a draw!")
            break

        # Move to the next player
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
