import os
import random
import string

# === CONSTANTS ===
NUM_ROWS = 6
NUM_COLS = 7
MAX_COLS = 26  # Max columns supported (A-Z)
NUM_PLAYERS = 2  # Set to 2 for submission

CHECKERS = ['X', 'O', 'V', 'H', 'M']

# === CORE FUNCTIONS ===

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    """Creates a 2D list of empty spaces for the board."""
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board, cols):
    """Prints the board according to the specs."""
    col_labels = [string.ascii_uppercase[i] for i in range(cols)]
    print("  " + "   ".join(col_labels))
    print("+" + "+---"*cols + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "+---"*cols + "+")

def get_player_checkers(num_players):
    """Returns a list of checker symbols for the number of players."""
    return CHECKERS[:num_players]

def pick_starting_player(num_players):
    """Returns index (int) of first player."""
    return random.randint(0, num_players - 1)

def get_valid_column_input(player_checker, board, cols):
    """Prompts user until a valid column is entered."""
    valid_cols = [string.ascii_uppercase[i] for i in range(cols)]
    while True:
        col_input = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        if len(col_input) != 1 or col_input not in valid_cols:
            print(f"Invalid input. Please enter a letter between A and {valid_cols[-1]}.")
            continue
        col_idx = valid_cols.index(col_input)
        # Check for full column
        if board[0][col_idx] != ' ':
            print(f"Column {col_input} is full. Turn forfeited.")
            return None
        return col_idx

def place_checker(board, col, checker):
    """Places checker into the lowest empty spot in the given column."""
    for row in reversed(range(len(board))):
        if board[row][col] == ' ':
            board[row][col] = checker
            return row, col
    return None  # Shouldn't arrive here if input is validated

def check_win(board, row, col, checker, to_win = 4):
    """Checks all directions for a win after a move."""
    directions = [
        (0, 1),   # Horizontal
        (1, 0),   # Vertical
        (1, 1),   # Diagonal down
        (1, -1),  # Diagonal up
    ]
    for dr, dc in directions:
        count = 1
        # Forward direction
        r, c = row + dr, col + dc
        while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # Backward direction
        r, c = row - dr, col - dc
        while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        if count >= to_win:
            return True
    return False

def check_draw(board):
    """Returns True if the board is full."""
    for cell in board[0]:
        if cell == ' ':
            return False
    return True

# === MAIN GAME LOOP ===
def main():
    # Initialization
    board = create_board(NUM_ROWS, NUM_COLS)
    player_checkers = get_player_checkers(NUM_PLAYERS)
    current_player = pick_starting_player(NUM_PLAYERS)

    clear_screen()
    print_board(board, NUM_COLS)

    while True:
        player_checker = player_checkers[current_player]
        col_idx = get_valid_column_input(player_checker, board, NUM_COLS)
        clear_screen()
        if col_idx is not None:
            row_idx, col_idx = place_checker(board, col_idx, player_checker)
            print_board(board, NUM_COLS)
            # Check for win
            if check_win(board, row_idx, col_idx, player_checker):
                print(f"Player {player_checker} won!")
                break
            # Check draw
            if check_draw(board):
                print("The game is a draw!")
                break
        else:
            # Forfeited turn due to full column
            print_board(board, NUM_COLS)
        # Alternate to next player
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == '__main__':
    main()
