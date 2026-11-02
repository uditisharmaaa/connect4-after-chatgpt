import os
import random
import string
import sys

# ======= Configuration (Submission must be 6x7 with 2 players) =======
ROWS = 6
COLS = 7  # Max 26
NUM_PLAYERS = 2  # Supported: 2..5
CHECKERS = ['X', 'O', 'V', 'H', 'M']
WIN_LENGTH = 4
# ================================================================

def clear_screen():
    # Linux/Unix as per assignment
    os.system('clear')

def create_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def column_labels(cols):
    return [string.ascii_uppercase[i] for i in range(cols)]

def print_board(board):
    clear_screen()
    cols = len(board[0])
    labels = column_labels(cols)
    # Header
    header = '  ' + '   '.join(labels)
    print(header)
    print('+' + '---+' * cols)
    # Rows (top to bottom)
    for r in range(len(board)):
        row_str = '| ' + ' | '.join(board[r]) + ' |'
        print(row_str)
        print('+' + '---+' * cols)

def is_valid_column_input(inp, cols):
    if not inp or len(inp.strip()) != 1:
        return False
    ch = inp.strip().upper()
    labels = column_labels(cols)
    return ch in labels

def col_index_from_input(inp):
    return string.ascii_uppercase.index(inp.strip().upper())

def get_lowest_empty_row(board, col):
    # Return the row index (from bottom) where the checker will land, or None if full
    for r in reversed(range(len(board))):
        if board[r][col] == ' ':
            return r
    return None

def drop_checker(board, col, checker):
    row = get_lowest_empty_row(board, col)
    if row is None:
        return None  # Column full
    board[row][col] = checker
    return row

def in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols

def check_win_from_cell(board, start_r, start_c, dr, dc, checker):
    rows, cols = len(board), len(board[0])
    count = 0
    r, c = start_r, start_c
    while in_bounds(r, c, rows, cols) and board[r][c] == checker:
        count += 1
        if count >= WIN_LENGTH:
            return True
        r += dr
        c += dc
    return False

def check_win(board, last_r, last_c):
    # Only need to check around the last placed checker
    if last_r is None or last_c is None:
        return False
    checker = board[last_r][last_c]
    if checker == ' ':
        return False
    directions = [
        (0, 1),   # Horizontal right
        (1, 0),   # Vertical down
        (1, 1),   # Diagonal down-right
        (1, -1),  # Diagonal down-left
    ]
    rows, cols = len(board), len(board[0])

    # For each direction, slide back up to WIN_LENGTH-1 steps to cover sequences crossing the last move
    for dr, dc in directions:
        needed = WIN_LENGTH
        count = 0
        # Find the farthest starting point in the opposite direction
        r = last_r - (WIN_LENGTH - 1) * dr
        c = last_c - (WIN_LENGTH - 1) * dc
        # Iterate up to 2*(WIN_LENGTH-1) + 1 cells along the line
        for _ in range(WIN_LENGTH * 2 - 1 + max(rows, cols)):  # safe upper bound
            if not in_bounds(r, c, rows, cols):
                r += dr
                c += dc
                continue
            if board[r][c] == checker:
                count += 1
                if count >= needed:
                    return True
            else:
                count = 0
            # Stop if we've gone far enough past the last move in this direction
            # A simple bound to avoid infinite loop: break when we've moved past range where a 4-in-a-row including last move can exist
            # But given we used a big bound with in-bounds checks, we can terminate early if both ends are out-of-bounds,
            # still, the loop bound above is generous; we add an explicit end when we've advanced enough cells around last move.
            # To keep logic simple and safe, just continue until we exceed board bounds over a reasonable number of steps.
            r += dr
            c += dc
            # Heuristic early stop: If advancing far past last move by more than board size, break.
            # This prevents excessive iteration on large boards though our bound already prevents it.
        # Next direction
    return False

def check_draw(board):
    # Draw if no spaces left anywhere
    for row in board:
        if ' ' in row:
            return False
    return True

def next_player_index(current, total):
    return (current + 1) % total

def get_players(num_players):
    if not (2 <= num_players <= 5):
        raise ValueError("NUM_PLAYERS must be between 2 and 5")
    return CHECKERS[:num_players]

def prompt_input(player_checker, cols):
    labels = column_labels(cols)
    prompt = f"Player {player_checker}, please enter a column: "
    while True:
        try:
            inp = input(prompt)
        except EOFError:
            print("\nInput ended. Exiting game.")
            sys.exit(0)
        except KeyboardInterrupt:
            print("\nInterrupted. Exiting game.")
            sys.exit(0)

        if not is_valid_column_input(inp, cols):
            print(f"Invalid input. Please enter one of: {', '.join(labels)}")
            continue
        return inp.strip().upper()

def main():
    # Enforce column limit
    if COLS > 26:
        raise ValueError("Maximum supported columns is 26.")
    # Create players and board
    players = get_players(NUM_PLAYERS)
    board = create_board(ROWS, COLS)

    # Randomly select first player
    current_player_idx = random.randrange(len(players))

    # Show initial board
    print_board(board)

    last_move_r = None
    last_move_c = None

    while True:
        current_checker = players[current_player_idx]
        # Prompt for column input
        user_col_label = prompt_input(current_checker, COLS)
        col = col_index_from_input(user_col_label)

        # Attempt to drop checker
        drop_row = drop_checker(board, col, current_checker)
        if drop_row is None:
            # Column full; player loses turn
            print_board(board)
            print(f"Column {user_col_label} is full. Player {current_checker} loses the turn.")
            # No move recorded; advance to next player
            current_player_idx = next_player_index(current_player_idx, len(players))
            continue

        # Successful move: update last move
        last_move_r, last_move_c = drop_row, col

        # Print updated board
        print_board(board)

        # Check for win
        if check_win(board, last_move_r, last_move_c):
            print(f"Player {current_checker} won!")
            break

        # Check for draw
        if check_draw(board):
            print("It's a draw!")
            break

        # Next player's turn
        current_player_idx = next_player_index(current_player_idx, len(players))

if __name__ == "__main__":
    main()
