import os
import random
import sys

# ---- CONSTANTS ----
NUM_ROWS = 6                   # Must be <= 26
NUM_COLS = 7                   # Must be <= 26
MAX_COLS = 26
MAX_PLAYERS = 5
PLAYERS = ['X', 'O', 'V', 'H', 'M']  # Up to 5 players

NUM_PLAYERS = 2  # As per submission instructions
WIN_LENGTH = 4


# ---- FUNCTIONS ----

def clear_screen():
    os.system('clear')


def create_board(rows, cols):
    """Creates a board with given rows and columns, initialized with whitespace."""
    return [[' ' for _ in range(cols)] for _ in range(rows)]


def column_labels(cols):
    """Returns a list of column labels ('A', 'B', ..., ...) up to cols."""
    return [chr(ord('A') + i) for i in range(cols)]


def print_board(board):
    """Prints the board in the format specified."""
    cols = len(board[0])
    labels = column_labels(cols)
    print()
    print('  ' + '   '.join(labels))
    print('+' + '---+' * cols)
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+' + '---+' * cols)
    print()


def get_valid_column_input(board):
    """Prompts user for a column and validates input."""
    cols = len(board[0])
    valid_cols = column_labels(cols)
    while True:
        col_input = input().strip()
        if len(col_input) != 1:
            print("Invalid input. Please enter a single column letter:", end=' ')
            continue
        col_letter = col_input.upper()
        if col_letter not in valid_cols:
            print("Invalid input. Please enter a valid column letter:", end=' ')
            continue
        col_index = valid_cols.index(col_letter)
        # Check if the column is full
        if board[0][col_index] != ' ':
            print("Column is full. You lose your turn.")
            return None  # Special: lose turn if full
        return col_index


def drop_checker(board, col_idx, checker):
    """Drops a checker into the chosen column."""
    for row in reversed(board):
        if row[col_idx] == ' ':
            row[col_idx] = checker
            return board.index(row), col_idx   # Return row and col indices where checker was placed
    return None  # Column full (should be checked before call)


def is_winner(board, row, col, checker):
    """Checks if placing checker at (row, col) leads to a win."""
    directions = [
        (1, 0),   # vertical
        (0, 1),   # horizontal
        (1, 1),   # diagonal down-right
        (1, -1),  # diagonal down-left
    ]
    for dr, dc in directions:
        count = 1
        # Check forward direction
        r, c = row + dr, col + dc
        while 0 <= r < NUM_ROWS and 0 <= c < NUM_COLS and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # Check backward direction
        r, c = row - dr, col - dc
        while 0 <= r < NUM_ROWS and 0 <= c < NUM_COLS and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        if count >= WIN_LENGTH:
            return True
    return False


def is_draw(board):
    """Checks if the board is full (draw)."""
    return all(cell != ' ' for cell in board[0])


def main():
    clear_screen()
    # Setup
    if NUM_COLS > MAX_COLS or NUM_ROWS > MAX_COLS:
        print("Board dimensions must not exceed 26.")
        sys.exit(1)

    board = create_board(NUM_ROWS, NUM_COLS)
    players = PLAYERS[:NUM_PLAYERS]
    col_labels = column_labels(NUM_COLS)

    # Randomly select starting player
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)
    print("Starting Connect 4!")
    print(f"There are {NUM_PLAYERS} players: " + ', '.join(players))
    print(f"Randomly choosing first player: Player {players[current_player_idx]}")
    print_board(board)

    winner = None

    while True:
        player_checker = players[current_player_idx]
        print(f"Player {player_checker}, please enter a column:", end=' ')
        col_idx = get_valid_column_input(board)
        if col_idx is None:
            # Lose turn if column full
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            continue
        row_idx, _ = drop_checker(board, col_idx, player_checker)

        clear_screen()
        print_board(board)

        if is_winner(board, row_idx, col_idx, player_checker):
            print(f"Player {player_checker} won!")
            winner = player_checker
            break
        if is_draw(board):
            print("It's a draw!")
            break

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
