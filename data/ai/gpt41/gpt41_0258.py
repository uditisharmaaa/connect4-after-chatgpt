import os
import random
import string

# ----- CONSTANTS -----
ROWS = 6                   # Number of rows in the board
COLS = 7                   # Number of columns in the board (max 26 for A-Z)
NUM_PLAYERS = 2            # Number of players (from 2 to 5)
PLAYER_MARKS = ['X', 'O', 'V', 'H', 'M']  # Player checker marks
CONNECT_N = 4              # Number of checkers in a row needed to win

# Global constant for the blank cell
BLANK = " "

# ----- FUNCTIONS -----

def clear_screen():
    """
    Clears the terminal screen using the 'clear' command (Linux/Unix only).
    """
    os.system('clear')

def create_board(rows, cols):
    """
    Creates a 2D list representing the board.
    Each cell is initialized with a blank space.
    """
    return [[BLANK for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """
    Prints the board to the terminal in the specified format.
    Columns are labeled as A, B, ..., up to 'cols'.
    """
    rows = len(board)
    cols = len(board[0])

    # Print column labels
    col_labels = [f" {string.ascii_uppercase[i]} " for i in range(cols)]
    print(" " + "  ".join(col_labels))
    
    # Print top border
    print("+" + "---+" * cols)

    # Print each row
    for row in board:
        print("|" + "|".join(f" {cell} " for cell in row) + "|")
        print("+" + "---+" * cols)

def get_valid_column(board, prompt):
    """
    Prompts the user until a valid column label is input.
    Returns the zero-based index of the chosen column.
    If the column is full, returns None.
    """
    cols = len(board[0])
    valid_labels = [string.ascii_uppercase[i] for i in range(cols)]
    while True:
        col_input = input(prompt).strip().upper()
        if len(col_input) != 1 or col_input not in valid_labels:
            print(f"Invalid input. Please enter a column letter from A-{valid_labels[-1]}.")
            continue
        col_index = valid_labels.index(col_input)
        # Check if column is full
        if board[0][col_index] != BLANK:
            print("That column is full. You lose your turn.")
            return None
        return col_index

def place_checker(board, col, mark):
    """
    Places the player's checker in the lowest available row of the specified column.
    Returns the row index where the checker was placed.
    Assumes the column is not full.
    """
    rows = len(board)
    for row in reversed(range(rows)):
        if board[row][col] == BLANK:
            board[row][col] = mark
            return row
    # Should not reach here if called appropriately

def check_win(board, last_row, last_col, mark):
    """
    Checks if placing 'mark' at (last_row, last_col) makes a four-in-a-row in any direction.
    Returns True if win, False otherwise.
    """
    def count_direction(delta_row, delta_col):
        """Counts consecutive cells in one direction from the last placed mark."""
        r, c = last_row + delta_row, last_col + delta_col
        count = 0
        while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == mark:
            count += 1
            r += delta_row
            c += delta_col
        return count

    # Check all directions: horizontal, vertical, diagonals
    directions = [ (0,1), (1,0), (1,1), (1,-1) ] # right, down, down-right, down-left
    for dr, dc in directions:
        total = 1 # count the current checker
        total += count_direction(dr,  dc)
        total += count_direction(-dr, -dc)
        if total >= CONNECT_N:
            return True
    return False

def board_is_full(board):
    """
    Checks if the board is full (no blank spaces in the top row).
    """
    return all(cell != BLANK for cell in board[0])

def pick_random_player(num_players):
    """
    Randomly picks a player index from 0 to num_players-1.
    """
    return random.randint(0, num_players - 1)

def main():
    # --- Initialization ---
    board = create_board(ROWS, COLS)
    player_marks = PLAYER_MARKS[:NUM_PLAYERS]
    player = pick_random_player(NUM_PLAYERS)  # index of current player

    clear_screen()
    print_board(board)
    print(f"Player {player_marks[player]} begins!\n")

    # --- Game Loop ---
    while True:
        current_mark = player_marks[player]
        print(f"Player {current_mark}, please enter a column:")

        col = get_valid_column(board, "> ")

        if col is None:
            # If invalid due to full column, lose the turn
            player = (player + 1) % NUM_PLAYERS
            clear_screen()
            print_board(board)
            continue

        # Place the checker
        row = place_checker(board, col, current_mark)

        clear_screen()
        print_board(board)

        # Check for a win
        if check_win(board, row, col, current_mark):
            print(f"Player {current_mark} won!")
            break

        # Check for draw
        if board_is_full(board):
            print("The game is a draw!")
            break

        # Alternate player
        player = (player + 1) % NUM_PLAYERS

# --- Run the game ---
if __name__ == "__main__":
    main()
