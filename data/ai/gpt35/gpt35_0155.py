import os
import random
import string

# Constants (set for submission: 6 rows, 7 columns, 2 players)
ROWS = 6
COLUMNS = 7
PLAYERS = 2
WIN_LENGTH = 4

CHECKERS = ['X', 'O', 'V', 'H', 'M']  # Max 5 players allowed

def clear_screen():
    os.system('clear')

def create_board(rows, columns):
    return [[' ' for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    # Print column headers
    col_labels = [string.ascii_uppercase[i] for i in range(len(board[0]))]
    print('  ' + '   '.join(col_labels))
    # Print rows with separators
    for r in range(len(board)):
        print('+' + '---+' * len(board[0]))
        row_str = '|'
        for c in range(len(board[0])):
            row_str += ' ' + board[r][c] + ' |'
        print(row_str)
    print('+' + '---+' * len(board[0]))

def is_valid_column(col_input, max_columns):
    if len(col_input) != 1:
        return False
    if col_input not in string.ascii_uppercase[:max_columns]:
        return False
    return True

def get_column_index(col_input):
    return string.ascii_uppercase.index(col_input)

def is_column_full(board, col):
    return board[0][col] != ' '

def place_checker(board, col, checker):
    # Place checker at lowest available row in column
    for row in range(len(board)-1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = checker
            return row
    # Column full - shouldn't reach here if checked before
    return None

def check_win(board, player_checker, row, col):
    max_row = len(board)
    max_col = len(board[0])

    def count_direction(delta_r, delta_c):
        count = 1
        # forward direction
        r, c = row + delta_r, col + delta_c
        while 0 <= r < max_row and 0 <= c < max_col and board[r][c] == player_checker:
            count += 1
            r += delta_r
            c += delta_c
        # backward direction
        r, c = row - delta_r, col - delta_c
        while 0 <= r < max_row and 0 <= c < max_col and board[r][c] == player_checker:
            count += 1
            r -= delta_r
            c -= delta_c
        return count

    # Horizontal check
    if count_direction(0, 1) >= WIN_LENGTH:
        return True
    # Vertical check
    if count_direction(1, 0) >= WIN_LENGTH:
        return True
    # Diagonal (\) check
    if count_direction(1, 1) >= WIN_LENGTH:
        return True
    # Diagonal (/) check
    if count_direction(1, -1) >= WIN_LENGTH:
        return True

    return False

def board_full(board):
    return all(board[0][c] != ' ' for c in range(len(board[0])))

def main():
    board = create_board(ROWS, COLUMNS)
    players = CHECKERS[:PLAYERS]
    current_player_idx = random.randint(0, PLAYERS - 1)

    while True:
        clear_screen()
        print_board(board)
        current_checker = players[current_player_idx]
        print(f"Player {current_checker}, please enter a column:")

        # Get valid input
        while True:
            col_input = input().strip().upper()
            if not is_valid_column(col_input, COLUMNS):
                print(f"Invalid input. Please enter a column letter A-{string.ascii_uppercase[COLUMNS-1]}:")
                continue

            col = get_column_index(col_input)

            if is_column_full(board, col):
                # As per assignment, turn is lost if column full
                print(f"Column {col_input} is full. Turn lost.")
                placed_row = None
                break

            placed_row = place_checker(board, col, current_checker)
            break

        # Check if player placed checker
        if placed_row is not None:
            if check_win(board, current_checker, placed_row, col):
                clear_screen()
                print_board(board)
                print(f"Player {current_checker} won!")
                break

            if board_full(board):
                clear_screen()
                print_board(board)
                print("The game is a draw!")
                break

        current_player_idx = (current_player_idx + 1) % PLAYERS

if __name__ == "__main__":
    main()
