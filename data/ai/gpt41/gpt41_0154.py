import os
import random
import string

# --- Constants (for easy configuration) ---
ROWS = 6               # Number of rows of the board (default: 6)
COLS = 7               # Number of columns of the board (default: 7, max: 26)
NUM_PLAYERS = 2        # Number of players (between 2 and 5)
PLAYER_CHARS = ['X', 'O', 'V', 'H', 'M']  # List of players' checkers


def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')  # if on windows, use 'cls'


def create_board(rows, cols):
    """Creates a 2D board filled with whitespace."""
    return [[' ' for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    """Prints the board in the specified format."""
    # Print column headers (A, B, C, ..., up to number of columns)
    col_headers = '  ' + '   '.join(string.ascii_uppercase[:len(board[0])])
    print(col_headers)
    print('+' + '---+' * len(board[0]))

    # Print board rows, from top to bottom
    for row in board:
        print('| ' + ' | '.join(row) + ' |')
        print('+' + '---+' * len(board[0]))


def get_valid_columns(board):
    """Returns a list of indices of columns that have at least an empty cell (not full)."""
    cols = []
    for c in range(len(board[0])):
        if board[0][c] == ' ':
            cols.append(c)
    return cols


def get_player_move(board, player_char):
    """Prompts the current player for a valid move and returns the chosen column index."""
    valid_columns = get_valid_columns(board)
    valid_labels = [string.ascii_uppercase[idx] for idx in valid_columns]

    while True:
        move = input(f'Player {player_char}, please enter a column: ').strip().upper()
        if len(move) != 1 or move not in string.ascii_uppercase[:len(board[0])]:
            print('Invalid input. Please enter a valid column letter.')
            continue
        col = string.ascii_uppercase.index(move)
        if col not in valid_columns:
            if board[0][col] != ' ':
                print('That column is full. You lose your turn!')
                return None
            else:
                print('Invalid move. Please select a non-full column.')
            continue
        return col


def place_checker(board, col, player_char):
    """Places the player's checker in the specified column (at the lowest available row)."""
    for row in reversed(range(len(board))):
        if board[row][col] == ' ':
            board[row][col] = player_char
            return row, col
    return None, None  # Should not happen if column is valid


def check_winner(board, row, col, player_char):
    """Checks if placing a checker at (row, col) creates a win for the given player."""

    def count_direction(dx, dy):
        """Counts same player's checkers along a direction (delta x, delta y)."""
        count = 0
        r, c = row + dy, col + dx
        while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == player_char:
            count += 1
            r += dy
            c += dx
        return count

    # 4 directions: horizontal, vertical, diagonal /, diagonal \
    directions = [ (1, 0), (0, 1), (1, 1), (1, -1) ]
    for dx, dy in directions:
        count = 1  # the one just placed
        count += count_direction(dx, dy)
        count += count_direction(-dx, -dy)
        if count >= 4:
            return True
    return False


def is_board_full(board):
    """Checks if the board is full (no empty cells in the top row)."""
    return all(cell != ' ' for cell in board[0])


def main():
    # Validate player count and board dimension limits
    assert 2 <= NUM_PLAYERS <= 5, "Number of players must be between 2 and 5"
    assert 4 <= ROWS and 4 <= COLS <= 26, "Invalid board dimensions (4 <= size <= 26)"

    # Player checkers in order
    player_checkers = PLAYER_CHARS[:NUM_PLAYERS]
    board = create_board(ROWS, COLS)

    # Randomly select starting player
    current_player = random.randint(0, NUM_PLAYERS - 1)

    # Show the initial (empty) board
    clear_screen()
    print_board(board)

    winner = None
    while True:
        player_char = player_checkers[current_player]
        col = get_player_move(board, player_char)

        # If move is None, the column is full and turn skipped, advance player
        if col is None:
            current_player = (current_player + 1) % NUM_PLAYERS
            continue

        # Place checker and update board
        row, _ = place_checker(board, col, player_char)

        clear_screen()
        print_board(board)

        # Check win condition if the last move created 4 in a row
        if check_winner(board, row, col, player_char):
            print(f'Player {player_char} won!')
            break

        # Check for draw
        if is_board_full(board):
            print('Game over, it is a draw!')
            break

        # Next player's turn
        current_player = (current_player + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
