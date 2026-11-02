import os
import random
import string

# === CONSTANTS ===
BOARD_ROWS = 6
BOARD_COLS = 7 # must be <= 26
NUM_PLAYERS = 2 # between 2 and 5 inclusive
CHECKERS = ['X', 'O', 'V', 'H', 'M']

# === FUNCTIONS ===

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    """Create a board of given size filled with spaces"""
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Print the current state of the board."""
    clear_screen()
    cols = len(board[0])
    # Print column headers
    headers = '  ' + '   '.join(string.ascii_uppercase[:cols])
    print(headers)
    print('+' + '---+' * cols)
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+' + '---+' * cols)

def get_valid_columns(board):
    """Return a set of indices of columns that are not full."""
    cols = len(board[0])
    valid = set()
    for c in range(cols):
        if board[0][c] == ' ':
            valid.add(c)
    return valid

def column_char_to_index(char):
    """Map a column letter A, B, ... to a column index (0-based)"""
    c = char.upper()
    if c in string.ascii_uppercase:
        return ord(c) - ord('A')
    return -1

def get_player_input(player_checker, board):
    """Prompt user for column input and validate."""
    valid_cols = get_valid_columns(board)
    cols = len(board[0])
    while True:
        user_input = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter corresponding to a column.")
            continue
        col_idx = column_char_to_index(user_input)
        if not (0 <= col_idx < cols):
            print("Invalid input. Please enter a valid column letter.")
            continue
        if col_idx not in valid_cols:
            print("Column is full. You lose your turn.")
            return None
        return col_idx

def place_checker(board, col, checker):
    """Place a checker in the specified column. Returns row index or -1 if column is full."""
    for row in reversed(range(len(board))):
        if board[row][col] == ' ':
            board[row][col] = checker
            return row
    return -1

def check_win(board, row, col, checker):
    """Check if placing checker at (row, col) wins."""
    directions = [
        (0, 1),   # Horizontal
        (1, 0),   # Vertical
        (1, 1),   # Diagonal \
        (1, -1),  # Diagonal /
    ]
    rows = len(board)
    cols = len(board[0])
    for dr, dc in directions:
        count = 1
        # Check in the positive direction
        r, c = row + dr, col + dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # Check in the negative direction
        r, c = row - dr, col - dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        if count >= 4:
            return True
    return False

def check_draw(board):
    """Check if the board is drawn (no spaces in the top row)."""
    return all(cell != ' ' for cell in board[0])

def get_next_player(curr_idx, total_players):
    return (curr_idx + 1) % total_players

def main():
    board = create_board(BOARD_ROWS, BOARD_COLS)
    players = CHECKERS[:NUM_PLAYERS]
    current = random.randint(0, NUM_PLAYERS - 1)
    print_board(board)
    print(f"Player {players[current]} will start the game!")
    input("Press Enter to start...")
    while True:
        print_board(board)
        col = get_player_input(players[current], board)
        if col is None:
            # Column full, this player's turn is lost
            current = get_next_player(current, NUM_PLAYERS)
            continue
        row = place_checker(board, col, players[current])
        if check_win(board, row, col, players[current]):
            print_board(board)
            print(f"Player {players[current]} won!")
            break
        if check_draw(board):
            print_board(board)
            print("Game is a draw!")
            break
        current = get_next_player(current, NUM_PLAYERS)

if __name__ == "__main__":
    main()
