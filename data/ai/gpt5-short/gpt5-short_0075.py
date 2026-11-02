import os
import random
import sys

# -------------------------
# Configuration constants
# -------------------------
ROWS = 6
COLS = 7
COL_LABELS = [chr(ord('A') + i) for i in range(COLS)]  # ['A','B','C','D','E','F','G']

# Player tokens in the order they will rotate.
TOKENS = ['X', 'O', 'V', 'H', 'M']

# How many players are in this game (2 to 5).
NUM_PLAYERS = 2  # Change this to 3, 4, or 5 as desired.


# -------------------------
# Utility functions
# -------------------------
def clear_screen():
    # Per requirement, use 'clear'
    os.system('clear')


def create_board(rows=ROWS, cols=COLS):
    return [[' ' for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    # Column headers
    print('  ' + '   '.join(COL_LABELS))
    print('+' + '---+' * COLS)
    for r in range(ROWS):
        row_cells = []
        for c in range(COLS):
            row_cells.append(board[r][c])
        print('|' + '|'.join(f' {cell} ' for cell in row_cells) + '|')
        print('+' + '---+' * COLS)


def column_from_input(s):
    s = s.strip().upper()
    if len(s) != 1:
        return None
    if s in COL_LABELS:
        return COL_LABELS.index(s)
    return None


def is_column_full(board, col):
    return board[0][col] != ' '


def drop_piece(board, col, token):
    """
    Drops token into column col; returns the row index where it landed, or None if full.
    """
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = token
            return row
    return None


def in_bounds(r, c):
    return 0 <= r < ROWS and 0 <= c < COLS


def count_direction(board, start_r, start_c, dr, dc, token):
    """
    Count consecutive tokens starting just beyond (start_r, start_c) in direction (dr, dc).
    Does not count the starting cell itself.
    """
    r, c = start_r + dr, start_c + dc
    count = 0
    while in_bounds(r, c) and board[r][c] == token:
        count += 1
        r += dr
        c += dc
    return count


def is_winning_move(board, last_r, last_c):
    """
    After placing at (last_r, last_c), check if that created a 4-in-a-row.
    """
    token = board[last_r][last_c]
    if token == ' ':
        return False

    directions = [
        (0, 1),   # horizontal
        (1, 0),   # vertical
        (1, 1),   # diag down-right
        (1, -1),  # diag down-left
    ]
    for dr, dc in directions:
        total = 1  # start with the placed token
        total += count_direction(board, last_r, last_c, dr, dc, token)
        total += count_direction(board, last_r, last_c, -dr, -dc, token)
        if total >= 4:
            return True
    return False


def is_draw(board):
    # Draw if top row has no spaces (board completely full)
    return all(board[0][c] != ' ' for c in range(COLS))


def get_valid_num_players():
    # Ensure NUM_PLAYERS constant is valid with TOKENS length
    max_players = min(5, len(TOKENS))
    if not (2 <= NUM_PLAYERS <= max_players):
        print(f"NUM_PLAYERS must be between 2 and {max_players}. Found {NUM_PLAYERS}.")
        sys.exit(1)
    return NUM_PLAYERS


# -------------------------
# Main game loop
# -------------------------
def play_game():
    num_players = get_valid_num_players()
    players = TOKENS[:num_players]

    board = create_board()
    current_index = random.randrange(num_players)
    winner = None

    while True:
        clear_screen()
        print_board(board)
        current_player = players[current_index]
        print(f"Players: {', '.join(players)}  |  Turn: {current_player}")
        print("Enter column letter (A-G).")

        # Get input and validate
        col = None
        while True:
            user_in = input("Choose a column: ").strip()
            col = column_from_input(user_in)
            if col is None:
                print("Invalid input. Please enter a single letter A-G.")
                continue
            if is_column_full(board, col):
                print("That column is full. Choose another.")
                continue
            break

        # Place token
        row = drop_piece(board, col, current_player)

        # Check for win or draw
        if is_winning_move(board, row, col):
            winner = current_player
            clear_screen()
            print_board(board)
            print(f"Player {winner} wins! Congratulations!")
            break

        if is_draw(board):
            clear_screen()
            print_board(board)
            print("It's a draw!")
            break

        # Next player's turn
        current_index = (current_index + 1) % num_players

    print("Game over.")


if __name__ == "__main__":
    play_game()
