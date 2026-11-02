import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MIN_PLAYERS = 2
MAX_PLAYERS = 5
PLAYERS_COUNT = 2  # Must be between MIN_PLAYERS and MAX_PLAYERS
CHECKERS = ['X', 'O', 'V', 'H', 'M']
WIN_COUNT = 4


def clear_screen():
    os.system('clear')


def create_board(rows, columns):
    return [[' ' for _ in range(columns)] for _ in range(rows)]


def print_board(board):
    # Print column headers (A, B, C ...)
    header = '  ' + '   '.join(chr(ord('A') + i) for i in range(len(board[0])))
    print(header)
    # Print rows with separators
    line_sep = '+' + '---+' * len(board[0])
    for row in board:
        print(line_sep)
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
    print(line_sep)


def input_column(player_checker, columns):
    while True:
        user_input = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        # Validate input: single letter and in range
        if len(user_input) != 1:
            print(f"Invalid input: Enter a single letter from A to {chr(ord('A') + columns - 1)}.")
            continue
        col_index = ord(user_input) - ord('A')
        if col_index < 0 or col_index >= columns:
            print(f"Invalid input: Column {user_input} is out of range.")
            continue
        return col_index


def place_checker(board, col, checker):
    # Place checker at lowest empty row in col
    # If column full, return False, else True
    for row in reversed(range(len(board))):
        if board[row][col] == ' ':
            board[row][col] = checker
            return True
    return False  # column full


def check_win(board, checker):
    rows = len(board)
    cols = len(board[0])

    # Check horizontal
    for r in range(rows):
        count = 0
        for c in range(cols):
            if board[r][c] == checker:
                count += 1
                if count == WIN_COUNT:
                    return True
            else:
                count = 0

    # Check vertical
    for c in range(cols):
        count = 0
        for r in range(rows):
            if board[r][c] == checker:
                count += 1
                if count == WIN_COUNT:
                    return True
            else:
                count = 0

    # Check diagonal (/)
    for r in range(rows - WIN_COUNT + 1):
        for c in range(WIN_COUNT - 1, cols):
            count = 0
            for i in range(WIN_COUNT):
                if board[r + i][c - i] == checker:
                    count += 1
                else:
                    break
            if count == WIN_COUNT:
                return True

    # Check diagonal (\)
    for r in range(rows - WIN_COUNT + 1):
        for c in range(cols - WIN_COUNT + 1):
            count = 0
            for i in range(WIN_COUNT):
                if board[r + i][c + i] == checker:
                    count += 1
                else:
                    break
            if count == WIN_COUNT:
                return True

    return False


def check_draw(board):
    # No empty cells in top row means board full
    return all(cell != ' ' for cell in board[0])


def main():
    # Setup
    board = create_board(ROWS, COLUMNS)
    players = CHECKERS[:PLAYERS_COUNT]

    # Random starting player index
    current_player_idx = random.randint(0, PLAYERS_COUNT - 1)

    while True:
        clear_screen()
        print_board(board)
        current_checker = players[current_player_idx]

        col = input_column(current_checker, COLUMNS)

        if not place_checker(board, col, current_checker):
            # Column full: turn lost
            # No messages specified by assignment, but we keep the rule silently
            # Just skip the turn by continuing
            current_player_idx = (current_player_idx + 1) % PLAYERS_COUNT
            continue

        # Check win
        if check_win(board, current_checker):
            clear_screen()
            print_board(board)
            print(f"Player {current_checker} won!")
            break

        # Check draw
        if check_draw(board):
            clear_screen()
            print_board(board)
            print("The game is a draw!")
            break

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % PLAYERS_COUNT


if __name__ == '__main__':
    main()
