import os
import random
import string

# Constants
ROWS = 6
COLS = 7
MAX_COLS = 26
NUM_PLAYERS = 2  # can be from 2 to 5
PLAYER_TOKENS = ['X', 'O', 'V', 'H', 'M']  # Up to 5 players
EMPTY_CELL = ' '

# Set board dimensions and tokens based on NUM_PLAYERS and COLS
assert 2 <= NUM_PLAYERS <= len(PLAYER_TOKENS), "Number of players must be between 2 and 5."
assert 1 <= COLS <= MAX_COLS, "Columns must be between 1 and 26."

TOKENS = PLAYER_TOKENS[:NUM_PLAYERS]
COLUMN_LABELS = list(string.ascii_uppercase)[:COLS]


def clear_screen():
    os.system('clear')


def create_board(rows, cols):
    return [[EMPTY_CELL for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    # Print header
    print("\n  " + "   ".join(COLUMN_LABELS))
    # Print rows
    for r in range(ROWS):
        print("+---" * COLS + "+")
        print("| " + " | ".join(board[r]) + " |")
    print("+---" * COLS + "+")
    print()


def get_player_input(current_token, board):
    while True:
        inp = input(f"Player {current_token}, please enter a column: ").strip().upper()

        if len(inp) != 1 or inp not in COLUMN_LABELS:
            print(f"Invalid input! Enter one of: {', '.join(COLUMN_LABELS)}")
            continue

        col = COLUMN_LABELS.index(inp)
        if board[0][col] != EMPTY_CELL:
            print("That column is full! (You lose your turn.)")
            return None  # Signal for a lost turn

        return col


def drop_checker(board, col, token):
    # Place token in the lowest empty cell in the column
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == EMPTY_CELL:
            board[row][col] = token
            return row, col
    return None  # Should not happen (handled in get_player_input)


def is_winner(board, row, col, token):
    # Directions: (dr, dc)
    directions = [
        (0, 1),   # Horizontal
        (1, 0),   # Vertical
        (1, 1),   # Diagonal down-right
        (1, -1),  # Diagonal down-left
    ]

    for dr, dc in directions:
        count = 1  # include the placed checker itself

        # Check in the positive direction
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == token:
            count += 1
            r += dr
            c += dc

        # Check in the negative direction
        r, c = row - dr, col - dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == token:
            count += 1
            r -= dr
            c -= dc

        if count >= 4:
            return True

    return False


def is_draw(board):
    return all(cell != EMPTY_CELL for cell in board[0])


def main():
    board = create_board(ROWS, COLS)

    # Choose who starts first randomly
    current_player = random.randint(0, NUM_PLAYERS - 1)
    tokens = TOKENS

    clear_screen()
    print_board(board)

    while True:
        token = tokens[current_player]

        col = get_player_input(token, board)
        if col is None:
            # Player loses turn because column is full
            current_player = (current_player + 1) % NUM_PLAYERS
            continue

        row, col = drop_checker(board, col, token)

        clear_screen()
        print_board(board)

        if is_winner(board, row, col, token):
            print(f"Player {token} won!")
            break
        elif is_draw(board):
            print("It's a draw!")
            break

        # Next player's turn
        current_player = (current_player + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
