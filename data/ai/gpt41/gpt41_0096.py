import os
import random
import string

# Constants
ROWS = 6
COLUMNS = 7
MAX_COLUMNS = 26
NUM_PLAYERS = 2 # can be set to 2-5
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board, cols):
    clear_screen()
    # Print column labels
    col_labels = '  '
    for i in range(cols):
        col_labels += f' {chr(ord("A") + i)}  '
    print(col_labels)
    # Print board rows
    border = '+' + '---+' * cols
    for row in board:
        print(border)
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
    print(border)

def get_next_open_row(board, col):
    # Returns the index of the lowest empty row in the given column
    for row in reversed(range(len(board))):
        if board[row][col] == ' ':
            return row
    return None

def is_valid_column(col_input, cols):
    # Validates if input is a valid column letter within the board's columns
    if len(col_input) != 1:
        return False
    if col_input not in string.ascii_uppercase[:cols]:
        return False
    return True

def place_checker(board, row, col, checker):
    board[row][col] = checker

def check_for_win(board, checker):
    rows = len(board)
    cols = len(board[0])
    for r in range(rows):
        for c in range(cols):
            # Horizontal
            if c + 3 < cols and all(board[r][c+i] == checker for i in range(4)):
                return True
            # Vertical
            if r + 3 < rows and all(board[r+i][c] == checker for i in range(4)):
                return True
            # Diagonal down-right
            if r + 3 < rows and c + 3 < cols and all(board[r+i][c+i] == checker for i in range(4)):
                return True
            # Diagonal up-right
            if r - 3 >= 0 and c + 3 < cols and all(board[r-i][c+i] == checker for i in range(4)):
                return True
    return False

def is_board_full(board):
    return all(cell != ' ' for row in board for cell in row)

def main():
    # Game Setup
    cols = min(COLUMNS, MAX_COLUMNS)
    rows = ROWS
    num_players = min(max(2, NUM_PLAYERS), 5)
    checkers = CHECKERS[:num_players]
    board = create_board(rows, cols)

    first_player = random.randint(0, num_players - 1)
    current_player = first_player

    print_board(board, cols)

    while True:
        checker = checkers[current_player]
        print(f"Player {checker}, please enter a column:")

        # Player input and validation
        col_letter = input().strip().upper()

        while not is_valid_column(col_letter, cols) or \
              (get_next_open_row(board, ord(col_letter)-ord('A')) is None):
            if not is_valid_column(col_letter, cols):
                print("Invalid input. Please enter a valid column letter:")
            else:
                print("Column is full. Turn lost.")
                break
            col_letter = input().strip().upper()
        else:
            col_index = ord(col_letter) - ord('A')
            row_index = get_next_open_row(board, col_index)
            if row_index is not None:
                place_checker(board, row_index, col_index, checker)

        print_board(board, cols)

        # Check win
        if check_for_win(board, checker):
            print(f"Player {checker} won!")
            break

        # Check draw
        if is_board_full(board):
            print("It's a draw!")
            break

        if not is_valid_column(col_letter, cols) or \
           (get_next_open_row(board, ord(col_letter)-ord('A')) is None):
            # Current player loses turn ONLY if column is full
            current_player = (current_player + 1) % num_players
            continue

        # Next player's turn
        current_player = (current_player + 1) % num_players

if __name__ == "__main__":
    main()
