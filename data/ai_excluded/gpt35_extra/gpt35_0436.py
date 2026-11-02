import os
import random

# Constants - can be changed for different dimensions and players
ROWS = 6
COLUMNS = 7
MIN_PLAYERS = 2
MAX_PLAYERS = 5
PLAYERS = ['X', 'O', 'V', 'H', 'M']  # Available checkers

# For this assignment submission:
NUM_PLAYERS = 2
CHECKERS = PLAYERS[:NUM_PLAYERS]


def clear_screen():
    os.system('clear')


def create_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    clear_screen()
    cols = len(board[0])
    # Print column headers
    headers = [chr(ord('A') + i) for i in range(cols)]
    print('  ' + '   '.join(headers))
    print('+---' * cols + '+')
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+---' * cols + '+')


def is_valid_column(input_str, cols):
    if len(input_str) != 1:
        return False
    c = input_str.upper()
    if not ('A' <= c <= chr(ord('A') + cols - 1)):
        return False
    return True


def get_column_index(col_letter):
    return ord(col_letter.upper()) - ord('A')


def place_checker(board, col_idx, checker):
    """
    Place the checker in the lowest available space in column col_idx.
    Return True if placed, False if the column is full.
    """
    for row in range(len(board) - 1, -1, -1):
        if board[row][col_idx] == ' ':
            board[row][col_idx] = checker
            return True
    return False  # column full


def check_win(board, checker):
    rows = len(board)
    cols = len(board[0])
    line_len = 4

    # Horizontal check
    for r in range(rows):
        for c in range(cols - line_len + 1):
            if all(board[r][c + i] == checker for i in range(line_len)):
                return True

    # Vertical check
    for c in range(cols):
        for r in range(rows - line_len + 1):
            if all(board[r + i][c] == checker for i in range(line_len)):
                return True

    # Diagonal (down-right) check
    for r in range(rows - line_len + 1):
        for c in range(cols - line_len + 1):
            if all(board[r + i][c + i] == checker for i in range(line_len)):
                return True

    # Diagonal (down-left) check
    for r in range(rows - line_len + 1):
        for c in range(line_len - 1, cols):
            if all(board[r + i][c - i] == checker for i in range(line_len)):
                return True

    return False


def check_draw(board):
    # Draw if no space left in top row (all columns full)
    return all(cell != ' ' for cell in board[0])


def ask_player_move(board, player):
    cols = len(board[0])
    while True:
        move = input(f"Player {player}, please enter a column: ").strip().upper()
        if not is_valid_column(move, cols):
            # Invalid input format
            continue
        col_idx = get_column_index(move)
        if col_idx < 0 or col_idx >= cols:
            # Out of range though checked already
            continue
        # Check if column full
        if board[0][col_idx] != ' ':
            # Column full - player loses turn
            return None
        # Valid move
        return col_idx


def main():
    board = create_board(ROWS, COLUMNS)

    # Random first player
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)
    current_checker = CHECKERS[current_player_idx]

    print_board(board)

    while True:
        col_idx = ask_player_move(board, current_checker)
        if col_idx is None:
            # Column full - lose turn, just skip to next player
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            current_checker = CHECKERS[current_player_idx]
            print_board(board)
            continue
        placed = place_checker(board, col_idx, current_checker)
        # placed should be True here, because check in ask_player_move ensures space
        print_board(board)
        if check_win(board, current_checker):
            print(f"Player {current_checker} won!")
            break
        if check_draw(board):
            print("The game is a draw.")
            break
        # Next player
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
        current_checker = CHECKERS[current_player_idx]


if __name__ == "__main__":
    main()
