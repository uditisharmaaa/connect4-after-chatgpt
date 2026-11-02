import random
import os
import string

# ---------------- Constants ----------------
ROWS = 6                    # Number of rows on the board
COLUMNS = 7                 # Number of columns on the board (max 26)
MAX_COLUMNS = 26
MIN_PLAYERS = 2
MAX_PLAYERS = 5
PLAYERS = 2                 # Number of players: can be set between 2 and 5
CHECKER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']  # Checker symbols for up to 5 players

# ---------------- Functions ----------------

def clear_screen():
    """
    Clears the terminal screen using os.system('clear').
    """
    os.system('clear')

def create_board(rows, cols):
    """
    Creates and returns the initial empty board as a 2D list filled with ' ' (whitespace).
    """
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """
    Prints the current state of the board in the specified format, including column labels.
    """
    cols = len(board[0])
    # Print column header
    col_labels = [string.ascii_uppercase[i] for i in range(cols)]
    print('  ' + '   '.join(col_labels))
    print('+' + '---+' * cols)
    for row in board:
        print('|' + '|'.join(' {} '.format(cell) for cell in row) + '|')
        print('+' + '---+' * cols)

def get_player_symbols(num_players):
    """
    Returns a list of checker symbols to be used by each player in order.
    """
    assert MIN_PLAYERS <= num_players <= MAX_PLAYERS
    return CHECKER_SYMBOLS[:num_players]

def select_first_player(num_players):
    """
    Selects a random player index (0-based) to start.
    """
    return random.randint(0, num_players - 1)

def get_valid_columns(board):
    """
    Returns a set of valid column letters (not full).
    """
    valid = set()
    for c in range(len(board[0])):
        if board[0][c] == ' ':
            valid.add(string.ascii_uppercase[c])
    return valid

def get_player_input(valid_columns):
    """
    Gets a valid column input from the player.
    Re-prompts until a valid input (uppercase letter for a non-full column) is given.
    """
    while True:
        user_input = input().strip().upper()
        if len(user_input) == 1 and user_input in valid_columns:
            return user_input
        print(f"Invalid input. Valid columns: {', '.join(sorted(valid_columns))}. Try again:")

def place_checker(board, col_letter, checker):
    """
    Places the checker in the chosen column, returns (row, col) where placed, or None if column full.
    """
    col = string.ascii_uppercase.index(col_letter)
    for row in range(len(board)-1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = checker
            return (row, col)
    # This shouldn't happen due to earlier validation, but just in case.
    return None

def check_win(board, row, col, checker):
    """
    Check if placing the checker at (row, col) caused a win (4 in a row in any direction).
    Returns True if the player wins.
    """
    directions = [
        (0, 1),    # Horizontal right/left
        (1, 0),    # Vertical down/up
        (1, 1),    # Diagonal down-right/up-left
        (1, -1)    # Diagonal down-left/up-right
    ]
    for dr, dc in directions:
        count = 1  # Include the current placed checker
        # Check one direction
        r, c = row + dr, col + dc
        while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # Check the opposite direction
        r, c = row - dr, col - dc
        while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        if count >= 4:
            return True
    return False

def is_board_full(board):
    """
    Returns True if the board is full (draw), False otherwise.
    """
    for cell in board[0]:
        if cell == ' ':
            return False
    return True

# ---------------- Main Program ----------------

def main():
    # 1. Setup
    rows, cols = ROWS, COLUMNS
    num_players = PLAYERS
    # Defensive checks for board and players
    if not (2 <= num_players <= 5):
        raise ValueError("Number of players must be between 2 and 5.")
    if not (4 <= rows and 4 <= cols <= MAX_COLUMNS):
        raise ValueError("Board must be at least 4x4 and columns at most 26.")

    checker_symbols = get_player_symbols(num_players)
    board = create_board(rows, cols)
    current_player = select_first_player(num_players)

    # 2. Initial Board Print
    clear_screen()
    print_board(board)
    print(f"Player {checker_symbols[current_player]} starts!\n")

    # 3. Game Loop
    while True:
        valid_columns = get_valid_columns(board)
        current_checker = checker_symbols[current_player]
        print(f"Player {current_checker}, please enter a column:")

        # 4. Get and Validate Input
        col_letter = get_player_input(valid_columns)
        # Place checker, get position
        pos = place_checker(board, col_letter, current_checker)

        clear_screen()
        print_board(board)

        if pos is None:
            # This should NOT happen; possibly another race condition, but skip turn
            print(f"Column {col_letter} is full. Player {current_checker} loses the turn.")
        else:
            row, col = pos
            # 5. Check Win Condition
            if check_win(board, row, col, current_checker):
                print(f"Player {current_checker} won!")
                break
            # 6. Draw Condition
            if is_board_full(board):
                print("The board is full. It's a draw!")
                break

        # 7. Next Player (turn always advances, even for invalid/filled columns)
        current_player = (current_player + 1) % num_players

# ---------------- Run the Program ----------------

if __name__ == "__main__":
    main()
