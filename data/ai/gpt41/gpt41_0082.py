import os
import random
import string

# ------- CONSTANTS ---------
NUM_ROWS = 6
NUM_COLS = 7  # Max 26 (A-Z)
NUM_PLAYERS = 2  # Can set between 2 and 5

CHECKERS = ['X', 'O', 'V', 'H', 'M']

# -------- FUNCTIONS --------

def clear_screen():
    """
    Clears the terminal window.
    """
    os.system('clear')

def create_board(rows, cols):
    """
    Initializes the game board as a list of lists.
    """
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """
    Prints the board in a readable format.
    """
    cols = len(board[0])
    # Print the header (A, B, C, ...)
    col_labels = "  " + "   ".join(string.ascii_uppercase[:cols])
    print(col_labels)
    print("+" + "---+" * cols)
    
    # Print the board rows
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * cols)

def get_valid_columns(board):
    """
    Returns a list of column indices that are not full.
    """
    cols = len(board[0])
    valid_cols = []
    for col in range(cols):
        if board[0][col] == ' ':
            valid_cols.append(col)
    return valid_cols

def input_column(curr_player_checker, board):
    """
    Gets a valid column from user where to put their checker.
    Input must be an uppercase letter, within the column range and not full.
    If input is invalid, repeatedly prompt the player.
    """
    cols = len(board[0])
    valid_labels = list(string.ascii_uppercase[:cols])
    valid_col_indices = get_valid_columns(board)

    while True:
        col_input = input(f"Player {curr_player_checker}, please enter a column: ").strip().upper()
        if len(col_input) != 1 or col_input not in valid_labels:
            print("Invalid input! Please enter a valid column letter.")
            continue
        col_idx = ord(col_input) - ord('A')
        if col_idx not in valid_col_indices:
            print("Column is full or invalid. Try another column.")
            continue
        return col_idx

def drop_checker(board, col, checker):
    """
    Puts the checker in the lowest available row of the given column.
    Returns the row index where the checker was placed, or -1 if column is full.
    """
    for row in reversed(range(len(board))):  # from bottom-up
        if board[row][col] == ' ':
            board[row][col] = checker
            return row
    return -1  # Should not happen if column is already validated

def check_winner(board, checker, row, col):
    """
    Checks if placing the checker at (row, col) resulted in a win for that checker.
    Checks horizontally, vertically, both diagonals.
    """
    ROWS = len(board)
    COLS = len(board[0])
    directions = [
        (0, 1),    # Horizontal right
        (1, 0),    # Vertical down
        (1, 1),    # Diagonal down-right
        (1, -1)    # Diagonal down-left
    ]
    for dr, dc in directions:
        count = 1
        # Check in positive direction
        rr, cc = row + dr, col + dc
        while 0 <= rr < ROWS and 0 <= cc < COLS and board[rr][cc] == checker:
            count += 1
            rr += dr
            cc += dc
        # Check in negative direction
        rr, cc = row - dr, col - dc
        while 0 <= rr < ROWS and 0 <= cc < COLS and board[rr][cc] == checker:
            count += 1
            rr -= dr
            cc -= dc
        if count >= 4:
            return True
    return False

def check_draw(board):
    """
    Checks if the board is FULL (draw).
    """
    return all(cell != ' ' for cell in board[0])

def main():
    # Initial setup
    board = create_board(NUM_ROWS, NUM_COLS)
    player_checkers = CHECKERS[:NUM_PLAYERS]

    # Randomly select starting player
    curr_index = random.randint(0, NUM_PLAYERS-1)
    
    clear_screen()
    print_board(board)

    while True:
        curr_checker = player_checkers[curr_index]
        valid_cols = get_valid_columns(board)
        if not valid_cols:
            print("The game is a draw!")
            break

        # Get player's move and place checker
        col = input_column(curr_checker, board)
        row = drop_checker(board, col, curr_checker)

        clear_screen()
        print_board(board)

        # Check for win
        if check_winner(board, curr_checker, row, col):
            print(f"Player {curr_checker} won!")
            break

        # Check for draw (should not happen here since checked before move, but for safety)
        if check_draw(board):
            print("The game is a draw!")
            break

        # Next player's turn
        curr_index = (curr_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
