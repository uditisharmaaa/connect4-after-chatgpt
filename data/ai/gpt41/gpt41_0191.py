import os
import random
import string

# ======= CONSTANTS =======
ROWS = 6              # Number of rows on the board
COLUMNS = 7           # Number of columns on the board (max 26)
PLAYERS = 2           # Number of players (2-5)
CHECKERS = ['X', 'O', 'V', 'H', 'M']  # Player checker symbols
WIN_LENGTH = 4        # Number of checkers in a row needed to win
MAX_COLUMNS = 26      # Board supports up to 26 columns for labeling

# ======= BOARD CREATION & PRINTING =======

def create_board(rows, columns):
    """Return a 2D list with the specified dimensions, filled with spaces."""
    return [[' ' for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    """Prints the board to the terminal as specified."""
    os.system('clear')
    columns = len(board[0])
    # Print column labels
    col_labels = [string.ascii_uppercase[i] for i in range(columns)]
    print('  ' + '   '.join(col_labels))
    print('+' + '---+' * columns)
    # Print each row
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+' + '---+' * columns)

# ======= INPUT VALIDATION =======

def get_column_input(valid_columns):
    """Prompt user for column and validate input."""
    while True:
        inp = input("Please enter a column: ").strip().upper()
        if len(inp) != 1 or inp not in valid_columns:
            print(f"Invalid input! Valid columns are: {' '.join(valid_columns)}")
        else:
            return inp

# ======= GAME LOGIC =======

def drop_checker(board, column_idx, checker):
    """
    Drop a checker into the specified column, if possible.
    Args:
        board: list of lists
        column_idx: int, index of column (0-based)
        checker: char, player's checker symbol
    Returns:
        (bool, int): (True, row index placed at) if successfully placed;
        (False, None) otherwise (column full)
    """
    for row in reversed(range(len(board))):
        if board[row][column_idx] == ' ':
            board[row][column_idx] = checker
            return True, row
    return False, None  # Column full

def board_full(board):
    """Returns True if no empty spaces in the top row."""
    return all(cell != ' ' for cell in board[0])

def check_win(board, row, col, checker):
    """Check if placing checker at (row, col) resulted in a win."""
    directions = [
        (0, 1),   # Horizontal right
        (1, 0),   # Vertical down
        (1, 1),   # Diagonal down-right
        (1, -1)   # Diagonal down-left
    ]
    rows, cols = len(board), len(board[0])

    for dr, dc in directions:
        count = 1  # Number of consecutive checkers (including placed one)
        # Check in the +ve direction
        r, c = row + dr, col + dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r += dr
            c += dc

        # Check in the -ve direction
        r, c = row - dr, col - dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc

        if count >= WIN_LENGTH:
            return True
    return False

# ======= MAIN GAME LOOP =======

def main():
    # Set up board and players
    board = create_board(ROWS, COLUMNS)
    player_symbols = CHECKERS[:PLAYERS]

    # Randomly select starting player
    current_player = random.randint(0, PLAYERS-1)

    # Prepare valid column labels (A, B, ..., etc.)
    valid_columns = [string.ascii_uppercase[i] for i in range(COLUMNS)]

    print_board(board)
    print(f"Player {player_symbols[current_player]} begins!")

    while True:
        player_symbol = player_symbols[current_player]
        print_board(board)
        print(f"Player {player_symbol},", end=' ')
        col_label = get_column_input(valid_columns)
        col_idx = valid_columns.index(col_label)

        success, placed_row = drop_checker(board, col_idx, player_symbol)
        if not success:
            print(f"Column {col_label} is full! You lose your turn.")
            # Move to next player (lose turn)
            current_player = (current_player + 1) % PLAYERS
            continue

        # Check for victory
        if check_win(board, placed_row, col_idx, player_symbol):
            print_board(board)
            print(f"Player {player_symbol} won!")
            break

        if board_full(board):
            print_board(board)
            print("The game is a draw!")
            break

        # Next player's turn
        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
