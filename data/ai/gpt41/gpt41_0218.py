import os
import random
import string

# --------- Constants ---------
NUM_ROWS = 6      # Changeable for different dimensions
NUM_COLS = 7      # Changeable for different dimensions (max 26)
NUM_PLAYERS = 2   # Changeable for more than 2 players (max 5)

PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]  # Support up to 5 players
WIN_CONDITION = 4 # Number of checkers in a row to win

# --------- Functions ---------
def clear_screen():
    """Clear the terminal screen."""
    os.system('clear')

def create_board(rows, cols):
    """Initialize the game board as 2D list filled with spaces."""
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board, cols):
    """Print the board to the terminal in the proper format."""
    col_labels = '  '.join(string.ascii_uppercase[:cols])
    print(f"  {col_labels}")
    print("+" + "---+" * cols)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * cols)

def get_valid_columns(board):
    """Return a list of column indices where moves are possible."""
    valid_cols = []
    for col in range(len(board[0])):
        if board[0][col] == " ":
            valid_cols.append(col)
    return valid_cols

def col_letter_to_index(letter):
    """Convert column letter (A-G) to column index (0-6)."""
    if len(letter) == 1 and letter in string.ascii_uppercase:
        return ord(letter) - ord('A')
    return -1

def is_column_full(board, col):
    """Check if a column is full."""
    return board[0][col] != " "

def place_checker(board, col, symbol):
    """Place a checker in the given column for the player symbol."""
    for row in reversed(range(len(board))):
        if board[row][col] == " ":
            board[row][col] = symbol
            return row, col
    return None  # Should not occur if move is validated

def is_board_full(board):
    """Check if the board is full (no moves left)."""
    return all(cell != " " for cell in board[0])

def check_win(board, symbol):
    """Check the board for a win for the given symbol."""
    rows = len(board)
    cols = len(board[0])

    # Horizontal check
    for r in range(rows):
        count = 0
        for c in range(cols):
            count = count + 1 if board[r][c] == symbol else 0
            if count == WIN_CONDITION:
                return True

    # Vertical check
    for c in range(cols):
        count = 0
        for r in range(rows):
            count = count + 1 if board[r][c] == symbol else 0
            if count == WIN_CONDITION:
                return True

    # Diagonal (\) check
    for r in range(rows - WIN_CONDITION + 1):
        for c in range(cols - WIN_CONDITION + 1):
            if all(board[r + i][c + i] == symbol for i in range(WIN_CONDITION)):
                return True

    # Diagonal (/) check
    for r in range(WIN_CONDITION - 1, rows):
        for c in range(cols - WIN_CONDITION + 1):
            if all(board[r - i][c + i] == symbol for i in range(WIN_CONDITION)):
                return True

    return False

def get_player_column_input(board, player_symbol):
    """Prompt the player for a column until a valid column is entered."""
    cols = len(board[0])
    valid_col_indices = set(get_valid_columns(board))
    col_labels = string.ascii_uppercase[:cols]

    while True:
        inp = input(f"Player {player_symbol}, please enter a column: ").strip().upper()
        if len(inp) != 1:
            print("Please enter a single letter corresponding to a column.")
            continue
        if inp not in col_labels:
            print("Invalid column. Please enter a valid letter.")
            continue
        col = col_letter_to_index(inp)
        if col not in valid_col_indices:
            if col >= 0 and col < cols:
                print("That column is full. You lose your turn!")
                return None  # Signal column full
            else:
                print("Selection out of range.")
            continue
        return col

def main():
    # Set up game
    board = create_board(NUM_ROWS, NUM_COLS)
    player_symbols = PLAYER_SYMBOLS[:NUM_PLAYERS]

    first_player = random.randint(0, NUM_PLAYERS - 1)
    current_player = first_player

    clear_screen()
    print_board(board, NUM_COLS)
    print(f"Player {player_symbols[current_player]} starts!\n")

    # Game loop
    while True:
        col = get_player_column_input(board, player_symbols[current_player])

        if col is None:  # Column full - skip turn
            current_player = (current_player + 1) % NUM_PLAYERS
            continue

        row, _ = place_checker(board, col, player_symbols[current_player])

        clear_screen()
        print_board(board, NUM_COLS)

        # Check win
        if check_win(board, player_symbols[current_player]):
            print(f"Player {player_symbols[current_player]} won!")
            break

        # Check draw
        if is_board_full(board):
            print("The game is a draw!")
            break

        # Next player's turn
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
