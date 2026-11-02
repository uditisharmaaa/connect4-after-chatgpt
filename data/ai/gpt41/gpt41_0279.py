import os
import random
import string

# ==== CONSTANTS ====
NUM_ROWS = 6        # Board rows (default 6)
NUM_COLS = 7        # Board columns (default 7)
MAX_COLS = 26       # Maximum, for labeling (A-Z)
NUM_PLAYERS = 2     # Number of players (default 2)

CHECKERS = ['X', 'O', 'V', 'H', 'M']  # Up to 5 players

# ==== BOARD CREATION ====
def create_board(rows, cols):
    """Creates an empty board with all cells as whitespace ' '."""
    return [[' ' for _ in range(cols)] for _ in range(rows)]

# ==== PRINTING ====
def print_board(board):
    """Clears the screen and prints the board in Connect 4 format."""
    os.system('clear')  # For Windows use 'cls'
    cols = len(board[0])
    # Header with column letters
    header = '  ' + '   '.join(string.ascii_uppercase[:cols])
    print(header)
    # Separator
    print('+' + '---+' * cols)
    for row in board:
        row_str = "|" + "|".join(f" {cell} " for cell in row) + "|"
        print(row_str)
        print('+' + '---+' * cols)

# ==== INPUT VALIDATION ====
def valid_column_input(inp, cols):
    """Check if the input is a valid column letter within bounds."""
    if len(inp) != 1 or inp not in string.ascii_uppercase[:cols]:
        return False
    return True

def is_column_full(board, col_idx):
    """Returns True if the top cell of column is occupied."""
    return board[0][col_idx] != ' '

# ==== GAME LOGIC ====
def get_lowest_empty_row(board, col_idx):
    """Returns the lowest empty row index in a column, or None if column full."""
    for row in reversed(range(len(board))):
        if board[row][col_idx] == ' ':
            return row
    return None

def make_move(board, col_idx, checker):
    """Place checker in the lowest available position in column. Returns row index or None if full."""
    row_idx = get_lowest_empty_row(board, col_idx)
    if row_idx is not None:
        board[row_idx][col_idx] = checker
    return row_idx

def board_full(board):
    """Check if the board is full."""
    for cell in board[0]:
        if cell == ' ':
            return False
    return True

def check_win(board, checker, row, col):
    """Checks for a win for the player 'checker' at (row, col) in all directions."""
    directions = [(0,1), (1,0), (1,1), (1,-1)]  # horiz, vert, diag \, diag /
    for dr, dc in directions:
        count = 1
        # Check in the positive direction
        r, c = row+dr, col+dc
        while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # Check in the negative direction
        r, c = row-dr, col-dc
        while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        if count >= 4:
            return True
    return False

# ==== MAIN GAME LOOP ====
def main():
    # Limit dimensions and number of players
    rows = max(1, min(NUM_ROWS, 99))
    cols = max(1, min(NUM_COLS, MAX_COLS))
    num_players = max(2, min(NUM_PLAYERS, len(CHECKERS)))
    player_checkers = CHECKERS[:num_players]
    
    board = create_board(rows, cols)
    
    # Randomly select first player
    current_player = random.randint(0, num_players - 1)
    
    print_board(board)
    print(f"Player {player_checkers[current_player]} will start!")
    
    winner = None
    while True:
        checker = player_checkers[current_player]
        # Input loop
        while True:
            print_board(board)
            col_letter = input(f"Player {checker}, please enter a column: ").strip().upper()
            if not valid_column_input(col_letter, cols):
                print("Invalid input! Please use a valid column letter (e.g. A, B, ...).")
                continue
            col_idx = string.ascii_uppercase.index(col_letter)
            if is_column_full(board, col_idx):
                print("That column is full! You lose your turn.")
                break  # Invalid move, lose turn
            # Valid input and column has space
            row_idx = make_move(board, col_idx, checker)
            print_board(board)
            # Check for win
            if check_win(board, checker, row_idx, col_idx):
                winner = checker
            break
        if winner:
            print(f"Player {winner} won!")
            break
        if board_full(board):
            print("The game is a draw!")
            break
        # Next player
        current_player = (current_player + 1) % num_players

if __name__ == '__main__':
    main()
