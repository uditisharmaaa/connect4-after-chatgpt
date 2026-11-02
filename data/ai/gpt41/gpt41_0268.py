import os
import random
import string

# ==== CONSTANTS ====
ROWS = 6  # Number of rows (default 6)
COLUMNS = 7  # Number of columns (default 7, max up to 26)
NUM_PLAYERS = 2  # Number of players (default 2, can be up to 5)
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']  # Supported player tokens
WIN_COUNT = 4  # Number of consecutive tokens needed to win

# ==== BOARD INITIALIZATION AND PRINTING ====

def create_board(rows, columns):
    """Initialize a board with the given dimensions, filled with spaces."""
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    """Clear the terminal and print the current state of the board."""
    os.system('clear')  # ON WINDOWS: use 'cls'
    columns = len(board[0])
    # Print column labels (A, B, C, ...)
    labels = '  ' + '   '.join(string.ascii_uppercase[:columns])
    print(labels)
    # Print the board with lines
    sep = '+' + '---+' * columns
    for row in board:
        print(sep)
        print('| ' + ' | '.join(row) + ' |')
    print(sep)

# ==== PLAYER AND INPUT FUNCTIONS ====

def get_player_symbols(num_players):
    """Assign the correct symbols to the players."""
    return PLAYER_SYMBOLS[:num_players]

def get_valid_column_input(board):
    """Prompt player for a column and ensure it's valid input."""
    columns = len(board[0])
    valid_labels = string.ascii_uppercase[:columns]
    while True:
        inp = input(f"Please enter a column: ").strip().upper()
        # Validate only one character, in allowed range
        if len(inp) != 1 or inp not in valid_labels:
            print(f"Invalid input. Please enter a letter between A and {valid_labels[-1]}.")
            continue
        col = valid_labels.index(inp)
        # Check if column is full
        if board[0][col] != " ":
            print("This column is full! You lose your turn.")
            return None  # Indicate that the player loses their turn
        return col

# ==== GAME LOGIC ====

def place_checker(board, column, symbol):
    """Place checker in chosen column, at the lowest free row."""
    rows = len(board)
    for row in range(rows - 1, -1, -1):
        if board[row][column] == " ":
            board[row][column] = symbol
            return row, column
    # Should not reach here if we check for full column earlier
    return None

def is_within_board(row, col, rows, cols):
    """Check if a row,col pair is inside the board bounds."""
    return 0 <= row < rows and 0 <= col < cols

def check_direction(board, start_row, start_col, delta_row, delta_col, symbol):
    """Count consecutive symbols from a start in a certain direction (+ and -)."""
    rows = len(board)
    cols = len(board[0])
    count = 1  # Start with the just-placed checker

    # Check in positive direction
    r, c = start_row + delta_row, start_col + delta_col
    while is_within_board(r, c, rows, cols) and board[r][c] == symbol:
        count += 1
        r += delta_row
        c += delta_col

    # Check in negative direction
    r, c = start_row - delta_row, start_col - delta_col
    while is_within_board(r, c, rows, cols) and board[r][c] == symbol:
        count += 1
        r -= delta_row
        c -= delta_col

    return count

def check_for_win(board, row, col, symbol):
    """Check if placing at (row,col) causes a win for the player."""
    # Four directions: horizontal, vertical, two diagonals
    directions = [
        (0, 1),   # Horizontal (left-right)
        (1, 0),   # Vertical (up-down)
        (1, 1),   # Diagonal '\'
        (1, -1),  # Diagonal '/'
    ]
    for dr, dc in directions:
        if check_direction(board, row, col, dr, dc, symbol) >= WIN_COUNT:
            return True
    return False

def is_draw(board):
    """Check if the board is full and there's no winner."""
    return all(cell != " " for cell in board[0])  # If top row is fully occupied, board is full

# ==== MAIN GAME LOOP ====

def main():
    # Setup
    board = create_board(ROWS, COLUMNS)
    player_symbols = get_player_symbols(NUM_PLAYERS)
    player_names = [f"Player {s}" for s in player_symbols]
    # Randomly select a starting player (index)
    current_idx = random.randint(0, NUM_PLAYERS - 1)

    # Show the empty board before starting
    print_board(board)

    while True:
        symbol = player_symbols[current_idx]
        print(f"{player_names[current_idx]}'s turn ({symbol}):")
        col = get_valid_column_input(board)
        if col is None:
            # Full column: player loses turn
            current_idx = (current_idx + 1) % NUM_PLAYERS
            continue
        # Place checker in lowest possible row
        row, _ = place_checker(board, col, symbol)
        print_board(board)

        # Check for a win
        if check_for_win(board, row, col, symbol):
            print(f"{player_names[current_idx]} won!")
            break
        # Check for a draw
        if is_draw(board):
            print("It's a draw!")
            break

        # Next player's turn
        current_idx = (current_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
