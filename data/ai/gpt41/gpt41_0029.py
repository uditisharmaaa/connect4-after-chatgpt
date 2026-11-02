import os
import random
import string

# === CONSTANTS ===
ROWS = 6         # Board rows
COLS = 7         # Board columns (max 26)
NUM_PLAYERS = 2  # Number of players (2-5)
CHECKERS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]

def create_board(rows, cols):
    """Initialize a board with given rows and cols filled with whitespace"""
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Clear screen and print the board as per specs"""
    os.system('clear')
    cols = len(board[0])
    # Column headers
    header = '  ' + '   '.join(string.ascii_uppercase[:cols])
    print(header)
    print('+' + '---+' * cols)
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+' + '---+' * cols)

def get_next_row(board, col):
    """Return the lowest empty row index in a column or None if full"""
    for row in reversed(range(len(board))):
        if board[row][col] == " ":
            return row
    return None

def is_valid_column(board, col):
    """Return True if column exists and has empty cell"""
    return 0 <= col < len(board[0]) and board[0][col] == " "

def get_player_input(board, player_checker):
    """Ask current player for input, validate it, and return col index"""
    cols = len(board[0])
    col_letters = string.ascii_uppercase[:cols]
    while True:
        col_input = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        if len(col_input) != 1 or col_input not in col_letters:
            print("Invalid input! Please enter a valid column letter.")
            continue
        col = col_letters.index(col_input)
        if not is_valid_column(board, col):
            print("Column is full or invalid! Please try another column.")
            continue
        return col

def check_direction(board, row, col, dr, dc, symbol):
    """Check consecutive symbols in one direction"""
    total = 0
    r, c = row, col
    for _ in range(4):
        if 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == symbol:
            total += 1
            r += dr
            c += dc
        else:
            break
    return total == 4

def check_win(board, symbol):
    """Check all directions for 4 in a row for the given symbol"""
    for r in range(len(board)):
        for c in range(len(board[0])):
            if (board[r][c] == symbol and (
                check_direction(board, r, c, 0, 1, symbol) or     # Horizontal
                check_direction(board, r, c, 1, 0, symbol) or     # Vertical
                check_direction(board, r, c, 1, 1, symbol) or     # Diag down-right
                check_direction(board, r, c, 1, -1, symbol))):    # Diag down-left
                return True
    return False

def board_full(board):
    """Check if the board is completely full"""
    return all(cell != " " for cell in board[0])

def main():
    board = create_board(ROWS, COLS)
    current_player = random.randrange(NUM_PLAYERS)
    print_board(board)

    while True:
        player_checker = CHECKERS[current_player]
        # Input phase
        col = get_player_input(board, player_checker)
        row = get_next_row(board, col)
        if row is None:
            # Column full, lose turn
            print(f"Column is full! Player {player_checker} loses their turn.")
        else:
            board[row][col] = player_checker
        print_board(board)
        # Check for win/draw only if successfully placed
        if row is not None and check_win(board, player_checker):
            print(f"Player {player_checker} won!")
            break
        if board_full(board):
            print("The game is a draw!")
            break
        # Next player's turn
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
