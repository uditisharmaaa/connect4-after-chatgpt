import os
import random
import string
import sys

# ----- CONSTANT VARIABLES -----
NUM_ROWS = 6               # Number of rows for the board
NUM_COLS = 7               # Number of columns for the board
MAX_COLS = 26              # Maximum columns, so we can use letters A-Z
NUM_PLAYERS = 2            # Number of players (between 2 and 5)
CHECKERS = ['X', 'O', 'V', 'H', 'M']  # Markers for the players

# ----- INPUT VALIDATION CHECK -----
def is_valid_column(col_input, valid_cols):
    """
    Validates if the column input is exactly one uppercase letter in the valid range (A-G for 7 cols)
    """
    return len(col_input) == 1 and col_input in valid_cols

# ----- PRINT BOARD -----
def print_board(board, valid_cols):
    """
    Prints the game board as specified in the assignment.
    """
    # Clear the screen (Unix-based systems)
    os.system('clear')
    # Column headers
    header = '  ' + '   '.join(valid_cols)
    print(header)
    print('+---' * NUM_COLS + '+')
    for row in board:
        print('|' + '|'.join(' {0} '.format(cell) for cell in row) + '|')
        print('+---' * NUM_COLS + '+')

# ----- INIT BOARD -----
def create_board():
    """
    Initializes the board with whitespace in empty positions.
    """
    return [[' ' for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]

# ----- FIND ROW FOR INSERTING CHECKER -----
def get_next_row(board, col):
    """
    Returns the lowest available row index in a column, or None if the column is full.
    """
    for row in reversed(range(NUM_ROWS)):
        if board[row][col] == ' ':
            return row
    return None

# ----- DROP CHECKER -----
def drop_checker(board, col, checker):
    """
    Attempts to drop a checker into the specified column. Returns True if success, else False.
    """
    row = get_next_row(board, col)
    if row is not None:
        board[row][col] = checker
        return True, row
    else:
        return False, None

# ----- CHECK WIN -----
def check_for_win(board, last_row, last_col, checker):
    """
    Checks if the last move resulted in a win. Checks horizontally, vertically, and both diagonals.
    """
    # Directions: (delta_row, delta_col)
    directions = [
        (0, 1),   # Horizontal (right)
        (1, 0),   # Vertical (down)
        (1, 1),   # Diagonal (\)
        (1, -1)   # Diagonal (/)
    ]
    for dr, dc in directions:
        count = 1  # Include the last placed checker
        # Check one direction
        r, c = last_row + dr, last_col + dc
        while 0 <= r < NUM_ROWS and 0 <= c < NUM_COLS and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # Check the other direction
        r, c = last_row - dr, last_col - dc
        while 0 <= r < NUM_ROWS and 0 <= c < NUM_COLS and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        # Win!
        if count >= 4:
            return True
    return False

# ----- CHECK DRAW -----
def is_draw(board):
    """
    Returns True if the board is full (i.e., no empty cells in any column)
    """
    for col in range(NUM_COLS):
        if board[0][col] == ' ':
            return False
    return True

# ----- MAIN GAME LOOP -----
def main():
    # --- Set up game parameters ---
    board = create_board()
    valid_cols = [chr(ord('A') + i) for i in range(NUM_COLS)]  # ['A','B',...]
    players = [CHECKERS[i] for i in range(NUM_PLAYERS)]
    # Randomly select first player
    curr_player_idx = random.randint(0, NUM_PLAYERS - 1)
    print_board(board, valid_cols)
    print(f"Player {players[curr_player_idx]} goes first! Press Enter to start.")
    input()
    game_won = False

    while True:
        print_board(board, valid_cols)
        player_checker = players[curr_player_idx]
        prompt = f"Player {player_checker}, please enter a column: "
        col_input = input(prompt).strip().upper()
        # Input validation loop
        while not is_valid_column(col_input, valid_cols) or get_next_row(board, valid_cols.index(col_input)) is None and board[0][valid_cols.index(col_input)] != ' ':
            if not is_valid_column(col_input, valid_cols): 
                print(f"Invalid input. Please enter only one letter (A-{valid_cols[-1]}).")
            elif board[0][valid_cols.index(col_input)] != ' ':
                print(f"Column {col_input} is full. You lose your turn!")
                # Player loses turn, advance turn
                curr_player_idx = (curr_player_idx + 1) % NUM_PLAYERS
                break
            col_input = input(prompt).strip().upper()
        else: # Only executes if break wasn't called
            col = valid_cols.index(col_input)
            success, row = drop_checker(board, col, player_checker)
            if not success:
                # Shouldn't get here due to validation, but safe-guard
                print(f"Column {col_input} is full. You lose your turn!")
                curr_player_idx = (curr_player_idx + 1) % NUM_PLAYERS
                continue

            # Check for win from (row, col)
            if check_for_win(board, row, col, player_checker):
                print_board(board, valid_cols)
                print(f"Player {player_checker} won!")
                return

            if is_draw(board):
                print_board(board, valid_cols)
                print("Game is a draw!")
                return

            # Advance to next player
            curr_player_idx = (curr_player_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
