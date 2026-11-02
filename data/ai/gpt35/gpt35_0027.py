import os
import random
import string

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2  # between 2 and 5
CHECKERS = ['X', 'O', 'V', 'H', 'M']  # max 5 players allowed
WIN_LENGTH = 4

def clear_screen():
    os.system('clear')


def create_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    clear_screen()
    cols = len(board[0])
    rows = len(board)
    # Column headers
    header = '  ' + '   '.join(string.ascii_uppercase[:cols])
    print(header)
    # Row separator line
    sep_line = '+' + ('---+' * cols)
    for r in range(rows):
        print(sep_line)
        row_str = '|'
        for c in range(cols):
            row_str += ' ' + board[r][c] + ' |'
        print(row_str)
    print(sep_line)


def get_player_input(player_checker, board):
    cols = len(board[0])
    valid_letters = string.ascii_uppercase[:cols]

    while True:
        user_input = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        if len(user_input) != 1:
            # Invalid length input
            continue
        if user_input not in valid_letters:
            # Not a valid column letter
            continue
        col_idx = valid_letters.index(user_input)
        # Check if column full
        if board[0][col_idx] != ' ':
            # Column is full -> player loses the turn according to assignment
            return None
        return col_idx


def place_checker(board, col_idx, checker):
    """
    Places checker in given column, falling to lowest available position.
    Returns True if placed successfully, False if column is full.
    """
    rows = len(board)
    for r in range(rows - 1, -1, -1):
        if board[r][col_idx] == ' ':
            board[r][col_idx] = checker
            return True
    return False  # column full


def check_win(board, checker):
    """
    Checks if the given checker has four in a row horizontally, vertically,
    or diagonally. Returns True if win found, else False.
    """
    rows = len(board)
    cols = len(board[0])
    length = WIN_LENGTH

    # Horizontal check
    for r in range(rows):
        for c in range(cols - length + 1):
            if all(board[r][c + offset] == checker for offset in range(length)):
                return True

    # Vertical check
    for c in range(cols):
        for r in range(rows - length + 1):
            if all(board[r + offset][c] == checker for offset in range(length)):
                return True

    # Diagonal down-right check
    for r in range(rows - length + 1):
        for c in range(cols - length + 1):
            if all(board[r + offset][c + offset] == checker for offset in range(length)):
                return True

    # Diagonal up-right check
    for r in range(length - 1, rows):
        for c in range(cols - length + 1):
            if all(board[r - offset][c + offset] == checker for offset in range(length)):
                return True

    return False


def check_draw(board):
    return all(cell != ' ' for cell in board[0])


def main():
    # Initialize board and players
    board = create_board(ROWS, COLS)
    player_checkers = CHECKERS[:PLAYERS]

    # Randomly select starting player
    current_player_idx = random.randint(0, PLAYERS - 1)

    print_board(board)

    while True:
        checker = player_checkers[current_player_idx]

        col = get_player_input(checker, board)
        if col is None:
            # Column full - per assignment: player loses the turn
            # Inform player and switch to next
            print(f"Column full! Player {checker} loses the turn.")
            # Pause before next turn
            input("Press Enter to continue...")
            current_player_idx = (current_player_idx + 1) % PLAYERS
            print_board(board)
            continue

        placed = place_checker(board, col, checker)
        # placed should always be True here because place_checker double checks,
        # but just be safe:
        if not placed:
            # Technically shouldn't occur because get_player_input rejects full cols
            print(f"Column full! Player {checker} loses the turn.")
            input("Press Enter to continue...")
            current_player_idx = (current_player_idx + 1) % PLAYERS
            print_board(board)
            continue

        print_board(board)

        # Check for win
        if check_win(board, checker):
            print(f"Player {checker} won!")
            break

        # Check for draw
        if check_draw(board):
            print("The game is a draw!")
            break

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % PLAYERS


if __name__ == '__main__':
    main()
