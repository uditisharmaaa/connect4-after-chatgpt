import os
import random

# -------------------- CONSTANTS --------------------
BOARD_ROWS = 6
BOARD_COLS = 7  # max 26
NUM_PLAYERS = 2  # can be between 2 and 5
CHECKERS = ['X', 'O', 'V', 'H', 'M']  # For up to 5 players

# --------------- BOARD INITIALIZATION --------------
def create_board():
    """Creates and returns a board with BOARD_ROWS x BOARD_COLS, all cells empty (' ')."""
    board = [[' ' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
    return board

# ------------------ PRINT BOARD --------------------
def print_board(board, player_checkers):
    """Clears the terminal and prints the board with column labels."""
    os.system('clear')
    # Print columns headers
    headers = '  '
    for c in range(BOARD_COLS):
        headers += ' ' + chr(ord('A') + c) + '  '
    print(headers)
    print('+' + '---+' * BOARD_COLS)
    for row in board:
        row_str = '|'
        for cell in row:
            row_str += ' ' + cell + ' |'
        print(row_str)
        print('+' + '---+' * BOARD_COLS)

# ----------------- INPUT VALIDATION ----------------
def get_valid_column(board, current_checker):
    """
    Prompts player for a valid column letter.
    Returns column index or None if full (loses turn).
    """
    while True:
        col = input(f"Player {current_checker}, please enter a column: ").strip().upper()
        if len(col) != 1 or not col.isalpha():
            print("Invalid input! Please type a single uppercase letter (A-G).")
            continue
        idx = ord(col) - ord('A')
        if idx < 0 or idx >= BOARD_COLS:
            print(f"Invalid column! Please enter between A and {chr(ord('A') + BOARD_COLS - 1)}.")
            continue
        # Check if the column is full
        if board[0][idx] != ' ':
            print("Column is full! You lose your turn.")
            return None
        return idx

# -------------- PLACE CHECKER IN BOARD -------------
def place_checker(board, col_index, checker):
    """
    Attempts to place a checker in the specified column.
    Returns the row, col of the placed checker (tuple).
    """
    for r in range(BOARD_ROWS-1, -1, -1):
        if board[r][col_index] == ' ':
            board[r][col_index] = checker
            return r, col_index
    # This should not happen if input validation is good!
    return None, None

# ------------ CHECK FOR WIN ("FOUR IN A ROW") -----------
def check_for_win(board, row, col, checker):
    """
    Checks if placing a checker at (row, col) leads to a win for that player.
    Four directions: horizontal, vertical, diagonals (/ and \).
    """
    directions = [
        (0, 1),   # Horizontal: right
        (1, 0),   # Vertical: down
        (1, 1),   # Diagonal: down-right
        (1, -1)   # Diagonal: down-left
    ]
    for dr, dc in directions:
        count = 1  # placed checker itself
        # Forward direction
        r, c = row + dr, col + dc
        while 0 <= r < BOARD_ROWS and 0 <= c < BOARD_COLS and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # Backward direction
        r, c = row - dr, col - dc
        while 0 <= r < BOARD_ROWS and 0 <= c < BOARD_COLS and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        if count >= 4:
            return True
    return False

# --------------- CHECK FOR DRAW --------------------
def is_draw(board):
    """True if no empty spaces in top row (i.e., board is full)."""
    for cell in board[0]:
        if cell == ' ':
            return False
    return True

# ---------------------- MAIN GAME -------------------------
def main():
    # Game setup
    board = create_board()
    player_checkers = CHECKERS[:NUM_PLAYERS]
    player_names = [f"Player {ckr}" for ckr in player_checkers]
    current_player_index = random.randint(0, NUM_PLAYERS - 1)

    print_board(board, player_checkers)
    print(f"{player_names[current_player_index]} goes first!")
    input("Press Enter to start the game...")

    # Game loop
    game_over = False
    while not game_over:
        print_board(board, player_checkers)
        cur_checker = player_checkers[current_player_index]
        col_index = get_valid_column(board, cur_checker)
        # If column full, skip to next player
        if col_index is None:
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            continue
        # Place checker
        row, col = place_checker(board, col_index, cur_checker)
        print_board(board, player_checkers)
        # Check for win
        if check_for_win(board, row, col, cur_checker):
            print(f"Player {cur_checker} won!")
            game_over = True
            continue
        # Check for draw
        if is_draw(board):
            print("The game is a draw!")
            game_over = True
            continue
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == '__main__':
    main()
