import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']  # Supports up to 5 players
WIN_COUNT = 4
COLUMN_LETTERS = [chr(ord('A') + i) for i in range(COLS)]


def clear_screen():
    os.system('clear')


def create_board(rows=ROWS, cols=COLS):
    """Create a rows x cols board filled with ' '."""
    return [[' ' for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    """Print the board as specified."""
    # Header
    print('  ' + '   '.join(COLUMN_LETTERS))
    print('+' + '---+' * len(board[0]))
    # Rows (top row index 0, bottom row index ROWS-1)
    for row in range(len(board)):
        print('|' + '|'.join(f' {board[row][col]} ' for col in range(len(board[0]))) + '|')
        print('+' + '---+' * len(board[0]))


def valid_column_input(column_input, cols=COLS):
    """Check if input is a single uppercase letter in range A..(A+cols-1)"""
    return (len(column_input) == 1 and
            column_input in COLUMN_LETTERS)


def get_column_index(column_letter):
    """Convert column letter to index."""
    return ord(column_letter) - ord('A')


def place_checker(board, col, checker):
    """
    Place the checker in the lowest free row of column col.
    Return True if placed, else False if column full.
    """
    for row in reversed(range(len(board))):
        if board[row][col] == ' ':
            board[row][col] = checker
            return True
    return False


def board_full(board):
    """Check if board is full - no empty spaces in top row."""
    return all(cell != ' ' for cell in board[0])


def check_winner(board, checker):
    rows = len(board)
    cols = len(board[0])

    # Check horizontal
    for row in range(rows):
        count = 0
        for col in range(cols):
            if board[row][col] == checker:
                count += 1
                if count == WIN_COUNT:
                    return True
            else:
                count = 0

    # Check vertical
    for col in range(cols):
        count = 0
        for row in range(rows):
            if board[row][col] == checker:
                count += 1
                if count == WIN_COUNT:
                    return True
            else:
                count = 0

    # Check diagonal (top-left to bottom-right)
    for row in range(rows - WIN_COUNT + 1):
        for col in range(cols - WIN_COUNT + 1):
            if all(board[row + i][col + i] == checker for i in range(WIN_COUNT)):
                return True

    # Check anti-diagonal (top-right to bottom-left)
    for row in range(rows - WIN_COUNT + 1):
        for col in range(WIN_COUNT - 1, cols):
            if all(board[row + i][col - i] == checker for i in range(WIN_COUNT)):
                return True

    return False


def main():
    board = create_board()
    players = CHECKERS[:PLAYERS]

    current_player_idx = random.randint(0, PLAYERS - 1)

    while True:
        clear_screen()
        print_board(board)
        current_checker = players[current_player_idx]
        print(f'Player {current_checker}, please enter a column:')

        # Input validation loop
        while True:
            user_input = input().strip().upper()
            if not valid_column_input(user_input):
                print(f'Invalid input. Please enter a column letter from A to {COLUMN_LETTERS[-1]}:')
                continue

            col_idx = get_column_index(user_input)
            # Check if column is full
            if board[0][col_idx] != ' ':
                # Turn is lost if column full
                print(f'Column {user_input} is full. You lose your turn.')
                placed = False
                break
            else:
                placed = place_checker(board, col_idx, current_checker)
                break

        if placed:
            # Check win
            if check_winner(board, current_checker):
                clear_screen()
                print_board(board)
                print(f'Player {current_checker} won!')
                return

            # Check draw
            if board_full(board):
                clear_screen()
                print_board(board)
                print('The game is a draw.')
                return

        # Rotate to next player
        current_player_idx = (current_player_idx + 1) % PLAYERS


if __name__ == '__main__':
    main()
