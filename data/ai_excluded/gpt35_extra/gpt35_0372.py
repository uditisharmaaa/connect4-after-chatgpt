import os
import random
import sys

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']
WIN_COUNT = 4
COL_LABELS = [chr(ord('A') + i) for i in range(COLS)]  # ['A', 'B', ...]


def clear_screen():
    os.system('clear')


def create_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    clear_screen()
    # Print column headers
    print('  ' + '   '.join(COL_LABELS))
    # Print rows with separators
    for r in range(len(board)):
        print('+' + '---+' * len(board[0]))
        print('|' + '|'.join(f' {board[r][c]} ' for c in range(len(board[0)])) + '|')
    print('+' + '---+' * len(board[0]))


def get_valid_column_input(player_checker):
    while True:
        user_input = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        if len(user_input) != 1:
            # must be exactly one char
            continue
        if user_input not in COL_LABELS:
            continue
        return COL_LABELS.index(user_input)


def place_checker(board, col, checker):
    # Place checker in lowest available row in column
    for row in range(len(board) - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = checker
            return row, col
    # Column full
    return -1, -1


def check_win(board, row, col, checker):
    directions = [
        (0, 1),   # horizontal right
        (1, 0),   # vertical down
        (1, 1),   # diagonal down-right
        (1, -1),  # diagonal down-left
    ]

    for dr, dc in directions:
        count = 1
        # Check positive direction
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # Check negative direction
        r, c = row - dr, col - dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc

        if count >= WIN_COUNT:
            return True
    return False


def check_draw(board):
    # If any cell in top row is empty, board not full
    return all(board[0][c] != ' ' for c in range(COLS))


def main():
    board = create_board(ROWS, COLS)
    players = CHECKERS[:NUM_PLAYERS]

    # Random starting player index
    current_player_index = random.randint(0, NUM_PLAYERS - 1)

    print_board(board)

    while True:
        checker = players[current_player_index]
        col = get_valid_column_input(checker)

        row, placed_col = place_checker(board, col, checker)
        if row == -1:
            # Column full - lose turn
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            print_board(board)
            continue

        print_board(board)

        if check_win(board, row, placed_col, checker):
            print(f"Player {checker} won!")
            sys.exit(0)

        if check_draw(board):
            print("Game is a draw!")
            sys.exit(0)

        current_player_index = (current_player_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
