import os
import random
import string

# --- CONSTANTS ---
ROWS = 6
COLS = 7  # Max 26 columns
PLAYER_CHARS = ['X', 'O', 'V', 'H', 'M']
NUM_PLAYERS = 2  # Change up to 5 if needed

# --- FUNCTIONS ---

def create_board(rows, cols):
    """Creates a board filled with spaces."""
    board = []
    for _ in range(rows):
        board.append([' '] * cols)
    return board

def print_board(board):
    """Prints the game board neatly."""
    os.system('clear')  # Use 'cls' on Windows, 'clear' on Unix
    col_labels = list(string.ascii_uppercase)[:len(board[0])]
    # Print column labels
    print('  ', end='')
    for col in col_labels:
        print(f' {col}  ', end='')
    print()
    # Print upper border
    print('+---' * len(board[0]) + '+')
    for row in board:
        print('|', end='')
        for cell in row:
            print(f' {cell} |', end='')
        print()
        # Print row separator
        print('+---' * len(board[0]) + '+')

def choose_first_player(num_players):
    """Randomly choose first player index."""
    return random.randint(0, num_players - 1)

def get_valid_column(board):
    """Prompts for a valid column. Returns the column index."""
    valid_cols = [chr(ord('A') + i) for i in range(len(board[0]))]
    while True:
        col_input = input("Please enter a column: ").strip().upper()
        if col_input not in valid_cols:
            print("Invalid column letter. Try again.")
            continue
        col = valid_cols.index(col_input)
        if board[0][col] != ' ':
            print("That column is full. If you choose it again, you lose your turn.")
        return col

def place_checker(board, col, player_char):
    """
    Places the player's checker in the selected column.
    Returns True if placement is successful, False if column is full (top occupied).
    """
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = player_char
            return True
    return False  # Column full

def check_win(board, player_char):
    """Checks if the player has 4 in a row anywhere on the board."""
    rows = len(board)
    cols = len(board[0])

    # Horizontal
    for r in range(rows):
        for c in range(cols - 3):
            if all(board[r][c + i] == player_char for i in range(4)):
                return True
    # Vertical
    for r in range(rows - 3):
        for c in range(cols):
            if all(board[r + i][c] == player_char for i in range(4)):
                return True
    # Diagonal (down-right)
    for r in range(rows - 3):
        for c in range(cols - 3):
            if all(board[r + i][c + i] == player_char for i in range(4)):
                return True
    # Diagonal (up-right)
    for r in range(3, rows):
        for c in range(cols - 3):
            if all(board[r - i][c + i] == player_char for i in range(4)):
                return True
    return False

def board_full(board):
    """Returns True if the board is full."""
    for cell in board[0]:
        if cell == ' ':
            return False
    return True

def main():
    board = create_board(ROWS, COLS)
    player_chars = PLAYER_CHARS[:NUM_PLAYERS]
    current_player = choose_first_player(NUM_PLAYERS)
    print_board(board)
    print(f"Player {player_chars[current_player]} goes first!")
    input("Press Enter to start...")

    turn_skipped = False
    while True:
        print_board(board)
        print(f"Player {player_chars[current_player]},", end=' ')
        col = get_valid_column(board)
        placed = place_checker(board, col, player_chars[current_player])
        if not placed:
            print("Column full! You lose your turn.")
            turn_skipped = True
        else:
            turn_skipped = False
            # Check for win
            if check_win(board, player_chars[current_player]):
                print_board(board)
                print(f"Player {player_chars[current_player]} won!")
                break
            if board_full(board):
                print_board(board)
                print("It's a draw!")
                break
        # Next player's turn
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
