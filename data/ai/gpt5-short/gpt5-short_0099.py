# Connect 4 (6x7) with 2–5 players for Intro CS
# - Columns labeled A–G
# - Players use symbols from PLAYER_SYMBOLS (X, O, V, H, M)
# - Number of players set by NUM_PLAYERS (2 to 5)
# - Random first player
# - Validates input and checks wins/draws
# - Uses os.system('clear') to refresh the screen

import os
import random
from typing import List, Optional, Tuple

# -----------------------------
# Configuration constants
# -----------------------------
ROWS = 6
COLS = 7
CONNECT_N = 4

# Symbols available for up to 5 players (in order)
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']

# Set how many players are playing (must be between 2 and 5)
NUM_PLAYERS = 2

# -----------------------------
# Utility and game functions
# -----------------------------

def clear_screen() -> None:
    # Requirement specifies using 'clear'
    os.system('clear')


def make_board(rows: int, cols: int) -> List[List[str]]:
    return [[' ' for _ in range(cols)] for _ in range(rows)]


def column_labels(cols: int) -> List[str]:
    # 'A' to 'G' for 7 columns
    return [chr(ord('A') + i) for i in range(cols)]


def print_board(board: List[List[str]]) -> None:
    labels = column_labels(COLS)
    print('  ' + '   '.join(labels))
    print('+' + '---+' * COLS)
    for r in range(ROWS):
        row_cells = []
        for c in range(COLS):
            row_cells.append(board[r][c])
        print('|' + '|'.join(f' {cell} ' for cell in row_cells) + '|')
        print('+' + '---+' * COLS)


def first_empty_row(board: List[List[str]], col: int) -> Optional[int]:
    # Return the bottommost empty row index in the given column, or None if full
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == ' ':
            return r
    return None


def drop_piece(board: List[List[str]], col: int, symbol: str) -> Optional[Tuple[int, int]]:
    r = first_empty_row(board, col)
    if r is None:
        return None
    board[r][col] = symbol
    return (r, col)


def in_bounds(r: int, c: int) -> bool:
    return 0 <= r < ROWS and 0 <= c < COLS


def count_direction(board: List[List[str]], r: int, c: int, dr: int, dc: int, symbol: str) -> int:
    # Count consecutive pieces of 'symbol' starting from (r, c) moving (dr, dc), not including (r, c)
    count = 0
    rr, cc = r + dr, c + dc
    while in_bounds(rr, cc) and board[rr][cc] == symbol:
        count += 1
        rr += dr
        cc += dc
    return count


def is_winner(board: List[List[str]], last_move: Tuple[int, int], symbol: str) -> bool:
    # Check the four directions around the last placed piece
    r, c = last_move
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]  # horiz, vert, diag down-right, diag down-left
    for dr, dc in directions:
        total = 1
        total += count_direction(board, r, c, dr, dc, symbol)
        total += count_direction(board, r, c, -dr, -dc, symbol)
        if total >= CONNECT_N:
            return True
    return False


def is_draw(board: List[List[str]]) -> bool:
    # Draw if no empty spaces in top row (i.e., all columns full)
    return all(board[0][c] != ' ' for c in range(COLS))


def get_validated_column_input(prompt: str) -> int:
    labels = column_labels(COLS)
    valid = set(labels)
    while True:
        raw = input(prompt).strip().upper()
        if len(raw) == 1 and raw in valid:
            return labels.index(raw)
        print(f"Invalid input. Please enter one of {', '.join(labels)}.")


def next_player_index(i: int, total: int) -> int:
    return (i + 1) % total


def validate_configuration() -> None:
    if not (2 <= NUM_PLAYERS <= 5):
        raise ValueError("NUM_PLAYERS must be between 2 and 5 inclusive.")
    if len(PLAYER_SYMBOLS) < NUM_PLAYERS:
        raise ValueError("PLAYER_SYMBOLS must contain at least NUM_PLAYERS symbols.")
    # Ensure symbols are single non-space characters
    for s in PLAYER_SYMBOLS[:NUM_PLAYERS]:
        if not isinstance(s, str) or len(s) != 1 or s == ' ':
            raise ValueError("Each player symbol must be a single, non-space character.")


def game_loop() -> None:
    validate_configuration()
    board = make_board(ROWS, COLS)
    players = PLAYER_SYMBOLS[:NUM_PLAYERS]
    current = random.randrange(NUM_PLAYERS)

    while True:
        clear_screen()
        print_board(board)
        print(f"Players: {', '.join(players)}  |  Current: {players[current]}")
        col = get_validated_column_input(f"Player {players[current]}, choose a column (A-{chr(ord('A')+COLS-1)}): ")

        row_to_drop = first_empty_row(board, col)
        if row_to_drop is None:
            print("That column is full. Press Enter to choose another.")
            input()
            continue

        last_move = drop_piece(board, col, players[current])
        assert last_move is not None  # we already checked

        if is_winner(board, last_move, players[current]):
            clear_screen()
            print_board(board)
            print(f"Player {players[current]} wins!")
            break

        if is_draw(board):
            clear_screen()
            print_board(board)
            print("It's a draw!")
            break

        current = next_player_index(current, NUM_PLAYERS)


def main() -> None:
    try:
        game_loop()
    except KeyboardInterrupt:
        print("\nGame interrupted. Goodbye!")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
