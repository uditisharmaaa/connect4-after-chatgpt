import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MIN_PLAYERS = 2
MAX_PLAYERS = 5
CHECKERS = ['X', 'O', 'V', 'H', 'M']
WIN_COUNT = 4

NUM_PLAYERS = 2  # Set number of players here (between MIN_PLAYERS and MAX_PLAYERS)
PLAYERS = CHECKERS[:NUM_PLAYERS]


def clear_screen():
    os.system('clear')


def create_board(rows, columns):
    return [[' ' for _ in range(columns)] for _ in range(rows)]


def print_board(board):
    clear_screen()
    # Print column labels
    labels = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    print('  ' + '   '.join(labels[:len(board[0])]))
    # Print top border
    print('+' + '---+' * len(board[0]))

    for row in board:
        line = '|'
        for cell in row:
            line += ' ' + cell + ' |'
        print(line)
        print('+' + '---+' * len(board[0]))


def get_column_index(column_char, max_columns):
    labels = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    if column_char in labels[:max_columns]:
        return labels.index(column_char)
    return -1


def is_valid_input(user_input, board):
    user_input = user_input.strip()
    if len(user_input) != 1 or not user_input.isalpha():
        return False
    col_idx = get_column_index(user_input.upper(), len(board[0]))
    if col_idx == -1:
        return False
    # Check if column is full
    if board[0][col_idx] != ' ':
        return False
    return True


def place_checker(board, col_idx, checker):
    # Place the checker in the lowest empty row in column col_idx
    for row_idx in range(len(board) - 1, -1, -1):
        if board[row_idx][col_idx] == ' ':
            board[row_idx][col_idx] = checker
            return row_idx, col_idx
    # If column is full, return None
    return None


def check_line(line, checker):
    count = 0
    for cell in line:
        if cell == checker:
            count += 1
            if count == WIN_COUNT:
                return True
        else:
            count = 0
    return False


def check_win(board, checker):
    rows = len(board)
    cols = len(board[0])

    # Check horizontal
    for r in range(rows):
        if check_line(board[r], checker):
            return True

    # Check vertical
    for c in range(cols):
        col = [board[r][c] for r in range(rows)]
        if check_line(col, checker):
            return True

    # Check diagonal "\" (top-left to bottom-right)
    for r in range(rows - WIN_COUNT + 1):
        for c in range(cols - WIN_COUNT + 1):
            diag = [board[r + i][c + i] for i in range(WIN_COUNT)]
            if all(cell == checker for cell in diag):
                return True

    # Check diagonal "/" (bottom-left to top-right)
    for r in range(WIN_COUNT - 1, rows):
        for c in range(cols - WIN_COUNT + 1):
            diag = [board[r - i][c + i] for i in range(WIN_COUNT)]
            if all(cell == checker for cell in diag):
                return True

    return False


def is_draw(board):
    # If no empty spaces in top row, board is full
    return all(cell != ' ' for cell in board[0])


def main():
    board = create_board(ROWS, COLUMNS)
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)

    while True:
        print_board(board)
        current_checker = PLAYERS[current_player_idx]
        print(f"Player {current_checker}, please enter a column:")

        while True:
            user_input = input().strip().upper()
            if not is_valid_input(user_input, board):
                # Invalid input: invalid char, out of range, or column full
                col_idx = get_column_index(user_input, COLUMNS)
                if col_idx != -1 and board[0][col_idx] != ' ':
                    # Column is full, lose turn
                    print(f"Column {user_input} is full. You lose your turn.")
                    break
                else:
                    print("Invalid input. Please enter a valid column letter:")
                continue
            else:
                col_idx = get_column_index(user_input, COLUMNS)
                pos = place_checker(board, col_idx, current_checker)
                break

        if pos is not None:
            # Check win
            if check_win(board, current_checker):
                print_board(board)
                print(f"Player {current_checker} won!")
                break

            # Check draw
            if is_draw(board):
                print_board(board)
                print("The game is a draw.")
                break

        # Switch player
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
