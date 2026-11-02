import os
import random
import string

# ---------------------- CONSTANTS ---------------------- #

# Board dimensions (modifiable for grading)
NUM_ROWS = 6
NUM_COLS = 7  # Should be <= 26 (A-Z)
NUM_PLAYERS = 2  # Can be 2 to 5 for grading; set to 2 for submission

CHECKERS = ['X', 'O', 'V', 'H', 'M']  # Player symbols
PLAYER_TOKENS = CHECKERS[:NUM_PLAYERS]

# ------------------------------------------------------- #

def clear_screen():
    os.system('clear')  # On Windows use 'cls'

def create_board(rows, cols):
    """Creates and returns a 2D board initialized with spaces."""
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Print the current board state."""
    clear_screen()
    cols = len(board[0])
    # Print column headers (A, B, ..., G, etc.)
    header = '  ' + '   '.join(string.ascii_uppercase[:cols])
    print(header)
    # Print horizontal border on top
    print('+' + '---+' * cols)
    for row in board:
        row_str = '| ' + ' | '.join(row) + ' |'
        print(row_str)
        print('+' + '---+' * cols)

def get_valid_columns(board):
    """Return a list of indices for columns where a move can be played (not full)."""
    return [col for col in range(len(board[0])) if board[0][col] == ' ']

def col_letter_to_index(letter):
    """Convert a column letter (A-Z) to an integer index, A=0, B=1, etc."""
    if letter in string.ascii_uppercase:
        return ord(letter) - ord('A')
    return -1

def index_to_col_letter(index):
    """Convert a column index to a letter, 0=A, 1=B, etc."""
    return chr(ord('A') + index)

def get_lowest_empty_row(board, col):
    """Return the lowest empty row index in a given column, or None if full."""
    for row in reversed(range(len(board))):
        if board[row][col] == ' ':
            return row
    return None

def get_player_move(player, board):
    """Prompt the player for a move and return the validated column index."""
    cols = len(board[0])
    col_letters = [index_to_col_letter(i) for i in range(cols)]
    prompt = f'Player {player}, please enter a column: '

    while True:
        move = input(prompt).strip().upper()
        if len(move) != 1 or move not in col_letters:
            print(f"Invalid input. Please enter a valid column ({', '.join(col_letters)}).")
            continue
        col = col_letter_to_index(move)
        if board[0][col] != ' ':
            print(f"Column {move} is full. You lose your turn.")
            return None  # Lose turn if column is full
        return col

def place_checker(board, col, checker):
    """Place the player's checker in the specified column, modifying the board."""
    row = get_lowest_empty_row(board, col)
    if row is not None:
        board[row][col] = checker
        return row
    return None

def check_direction(board, start_row, start_col, delta_row, delta_col, checker):
    """Return how many in a row of checker's symbol there are starting from the pos (excluding start)."""
    count = 0
    row, col = start_row + delta_row, start_col + delta_col
    rows, cols = len(board), len(board[0])
    while 0 <= row < rows and 0 <= col < cols and board[row][col] == checker:
        count += 1
        row += delta_row
        col += delta_col
    return count

def check_win(board, win_length=4):
    """Checks the whole board for any player win. Returns winner's checker or None."""
    rows, cols = len(board), len(board[0])
    for r in range(rows):
        for c in range(cols):
            if board[r][c] == ' ':
                continue
            checker = board[r][c]
            # Check all 4 directions: right, down, diag right-down, diag left-down
            for dr, dc in [(0,1), (1,0), (1,1), (1,-1)]:
                count = 1 + check_direction(board, r, c, dr, dc, checker) \
                          + check_direction(board, r, c, -dr, -dc, checker)
                if count >= win_length:
                    return checker
    return None

def check_draw(board):
    """Return True if the board is full, else False."""
    return all(cell != ' ' for cell in board[0])

def main():
    board = create_board(NUM_ROWS, NUM_COLS)
    print_board(board)

    # Select random player to begin
    current_player = random.randint(0, NUM_PLAYERS - 1)
    total_moves = 0
    max_moves = NUM_ROWS * NUM_COLS

    while True:
        checker = PLAYER_TOKENS[current_player]
        print_board(board)
        # Inform which player's turn
        print(f"\nPlayer {checker}, it's your turn.")

        valid_cols = get_valid_columns(board)

        if not valid_cols:
            print('Game is a draw! No more moves possible.')
            break

        col = get_player_move(checker, board)

        if col is None:  # Player loses turn due to full column
            current_player = (current_player + 1) % NUM_PLAYERS
            continue

        row = place_checker(board, col, checker)
        total_moves += 1

        winner = check_win(board)
        if winner:
            print_board(board)
            print(f'\nPlayer {winner} won!')
            break
        elif check_draw(board):
            print_board(board)
            print('Game is a draw!')
            break

        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == '__main__':
    main()
