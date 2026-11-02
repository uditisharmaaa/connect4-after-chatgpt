import os
import random
import sys

# ---- Constants ----
NUM_ROWS = 6            # Number of rows on the board (default 6)
NUM_COLS = 7            # Number of columns on the board (default 7; up to 26)
NUM_PLAYERS = 2         # Number of players (2-5 allowed)
WIN_LENGTH = 4          # Number of checkers in a row to win
MAX_COLS = 26           # Maximum board width

PLAYER_CHECKERS = ['X', 'O', 'V', 'H', 'M']  # Allowed checker symbols for players

assert 2 <= NUM_PLAYERS <= 5, "Game must support 2-5 players."
assert NUM_COLS <= MAX_COLS, f"Maximum columns supported: {MAX_COLS}"

def clear_screen():
    """Clears the terminal screen for better display."""
    os.system('clear' if os.name != 'nt' else 'cls')

def create_board(rows, cols):
    """Returns a 2D list representing a blank board."""
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Prints the current game board in Connect 4 style."""
    rows = len(board)
    cols = len(board[0])
    # Print column headers
    col_headers = '  ' + '   '.join(chr(ord('A') + c) for c in range(cols))
    print(col_headers)
    # Print horizontal border
    print('+' + '---+' * cols)
    # Print each row
    for r in range(rows):
        row_line = '| ' + ' | '.join(board[r][c] for c in range(cols)) + ' |'
        print(row_line)
        print('+' + '---+' * cols)

def is_valid_column(input_str, cols):
    """Checks if the input string is a valid column letter."""
    if len(input_str) != 1:
        return False
    if not input_str.isalpha() or not input_str.isupper():
        return False
    col_idx = ord(input_str) - ord('A')
    return 0 <= col_idx < cols

def get_valid_move(board, current_player_checker):
    """Prompts the player until a valid move is entered. Returns the col index or None if column is full."""
    cols = len(board[0])
    while True:
        move = input(f"Player {current_player_checker}, please enter a column: ").strip().upper()
        if not is_valid_column(move, cols):
            print(f"Invalid column '{move}'. Please enter a letter A-{chr(ord('A') + cols - 1)}.")
            continue
        col = ord(move) - ord('A')
        # Check if column is full
        if board[0][col] != ' ':
            print(f"Column '{move}' is full. Move is invalid and your turn is lost.")
            return None   # Turn is lost
        return col

def place_checker(board, col, checker):
    """Places the player's checker in the specified column at correct row."""
    for row in reversed(range(len(board))):  # Start from bottom row
        if board[row][col] == ' ':
            board[row][col] = checker
            return row, col
    return None, None  # Shouldn't happen if we check validity elsewhere

def check_for_win(board, checker):
    """Checks if the given checker has won (4 in a row in any direction)."""
    rows = len(board)
    cols = len(board[0])
    # Directions: (dr, dc): right, down, down-right, up-right
    directions = [(0, 1), (1, 0), (1, 1), (-1, 1)]
    for r in range(rows):
        for c in range(cols):
            if board[r][c] != checker:
                continue
            for dr, dc in directions:
                count = 1
                for k in range(1, WIN_LENGTH):
                    nr, nc = r + dr * k, c + dc * k
                    if 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] == checker:
                        count += 1
                    else:
                        break
                if count == WIN_LENGTH:
                    return True
    return False

def check_for_draw(board):
    """Returns True if the board has no empty cells on top row (i.e., board is full)."""
    return all(cell != ' ' for cell in board[0])

def main():
    # --- Initialization ---
    board = create_board(NUM_ROWS, NUM_COLS)
    player_checkers = PLAYER_CHECKERS[:NUM_PLAYERS]
    # Randomly select starting player
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)

    clear_screen()
    print_board(board)

    game_over = False
    while not game_over:
        current_checker = player_checkers[current_player_idx]

        move_col = get_valid_move(board, current_checker)
        if move_col is None:
            # Turn lost due to full column
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            continue

        # Place checker
        place_checker(board, move_col, current_checker)

        clear_screen()
        print_board(board)

        # Check for win condition
        if check_for_win(board, current_checker):
            print(f"Player {current_checker} won!")
            game_over = True
            break

        # Check for draw
        if check_for_draw(board):
            print("The game is a draw!")
            game_over = True
            break

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

if __name__ == '__main__':
    main()
