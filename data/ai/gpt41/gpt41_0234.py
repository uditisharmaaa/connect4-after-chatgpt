import os
import random
import sys

# ============================
# ===== Global Constants =====
# ============================

NUM_ROWS = 6                # Default number of rows
NUM_COLS = 7                # Default number of columns (max 26)
NUM_PLAYERS = 2             # Change to 2-5 as desired (for assignment: 2)
CONNECT_N = 4               # Number needed in a row to win
CHECKERS = ['X', 'O', 'V', 'H', 'M']  # Checker symbols for up to 5 players
EMPTY_CELL = ' '            # How empty cells are represented
LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

# ============================
# ===== Helper Functions =====
# ============================

def clear_screen():
    """Clear the terminal screen (works on Linux/Unix/Mac)."""
    os.system('clear')

def create_board(rows, cols):
    """Initialize the game board as a 2D list."""
    return [[EMPTY_CELL for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Print the current state of the board."""
    clear_screen()
    cols = len(board[0])
    # Print column header letters
    print('  ', end='')
    for c in range(cols):
        print(f' {LETTERS[c]} ', end='')
    print()
    # Print top border
    print('+' + '---+' * cols)
    # Print board rows
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+' + '---+' * cols)

def valid_column_input(input_str, cols):
    """Check if the input is a valid column letter within bounds."""
    return input_str in LETTERS[:cols]

def is_column_full(board, col_idx):
    """Check if a column is already full."""
    return board[0][col_idx] != EMPTY_CELL

def get_next_open_row(board, col_idx):
    """Return the row index of the lowest empty cell in a column (if any)."""
    for row in reversed(range(len(board))):
        if board[row][col_idx] == EMPTY_CELL:
            return row
    return None

def make_move(board, col_idx, checker):
    """
    Place the checker at the lowest available position of column col_idx.
    Return the row index, or None if the column is full.
    """
    row = get_next_open_row(board, col_idx)
    if row is not None:
        board[row][col_idx] = checker
        return row
    else:
        return None

def board_is_full(board):
    """Returns True if the board is full, False otherwise."""
    return all(cell != EMPTY_CELL for cell in board[0])

def in_bounds(row, col, rows, cols):
    """Returns True if the coordinates are inside the board."""
    return 0 <= row < rows and 0 <= col < cols

def check_win(board, row, col, checker):
    """Check if placing checker at (row,col) produced a win for that player."""
    directions = [
        (0, 1),      # horizontal right
        (1, 0),      # vertical down
        (1, 1),      # diagonal down-right
        (1, -1),     # diagonal down-left
    ]
    rows, cols = len(board), len(board[0])
    for dr, dc in directions:
        count = 1
        # Check in the positive direction
        r, c = row + dr, col + dc
        while in_bounds(r, c, rows, cols) and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # Check in the negative direction
        r, c = row - dr, col - dc
        while in_bounds(r, c, rows, cols) and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        if count >= CONNECT_N:
            return True
    return False

def select_starting_player(num_players):
    """Randomly select starting player from 0 to num_players-1."""
    return random.randint(0, num_players - 1)

def get_player_input(player_num, checker, cols):
    """Prompt the player for their move, validate input, and return column index."""
    while True:
        inp = input(f'Player {checker}, please enter a column: ').strip().upper()
        if len(inp) != 1 or not inp.isalpha():
            print("Invalid input. Please enter a single uppercase letter corresponding to a column.")
            continue
        if not valid_column_input(inp, cols):
            print("Invalid column. Please pick from the displayed column letters.")
            continue
        col_idx = LETTERS.index(inp)
        return col_idx

# ============================
# ===== Main Game Logic  =====
# ============================

def main():
    # Set up board and players
    board = create_board(NUM_ROWS, NUM_COLS)
    player_symbols = CHECKERS[:NUM_PLAYERS]
    player_names = ['Player ' + s for s in player_symbols]

    # Randomly choose which player starts
    current_player = select_starting_player(NUM_PLAYERS)

    # Print initial board
    print_board(board)
    print(f"{player_names[current_player]} ({player_symbols[current_player]}) starts!")

    # Main game loop
    turn_count = 0
    while True:
        checker = player_symbols[current_player]

        # Print board & prompt move
        print_board(board)
        print(f"It is {player_names[current_player]}'s turn ({checker}).")
        col_idx = get_player_input(current_player, checker, NUM_COLS)

        # Check if column is full
        if is_column_full(board, col_idx):
            print("That column is full and you lose your turn!")
            current_player = (current_player + 1) % NUM_PLAYERS
            continue

        # Place checker
        row_idx = make_move(board, col_idx, checker)
        turn_count += 1

        # Check for win
        if check_win(board, row_idx, col_idx, checker):
            print_board(board)
            print(f"{player_names[current_player]} won!")
            break

        # Check for draw
        if board_is_full(board):
            print_board(board)
            print("The game is a draw!")
            break

        # Next player's turn
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
