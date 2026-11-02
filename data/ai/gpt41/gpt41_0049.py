import os
import random

# ==== CONSTANTS ====
ROWS = 6
COLUMNS = 7
MAX_COLUMNS = 26
NUM_PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']
PLAYER_SYMBOLS = CHECKERS[:NUM_PLAYERS]
COLUMN_LABELS = [chr(ord('A') + i) for i in range(COLUMNS)]

# ==== FUNCTIONS ====

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    # Print column labels
    print('  ' + '   '.join(COLUMN_LABELS[:len(board[0])]))
    # Print top border
    print('+' + '---+' * len(board[0]))
    for row in board:
        print('|' + '|'.join(' {} '.format(cell) for cell in row) + '|')
        print('+' + '---+' * len(board[0]))

def get_valid_column(board, input_str):
    if len(input_str) != 1 or not input_str.isalpha():
        return -1
    input_str = input_str.upper()
    if input_str not in COLUMN_LABELS[:len(board[0])]:
        return -1
    col = COLUMN_LABELS.index(input_str)
    # If the topmost cell is filled, column is full
    if board[0][col] != ' ':
        return -2
    return col

def drop_checker(board, col, checker):
    # Place checker at the lowest empty spot in column
    for row in reversed(range(len(board))):
        if board[row][col] == ' ':
            board[row][col] = checker
            return row, col
    return None  # Should not happen if checked before

def check_victory(board, checker):
    rows = len(board)
    cols = len(board[0])
    for r in range(rows):
        for c in range(cols):
            if board[r][c] != checker:
                continue
            # Check horizontally
            if c <= cols - 4 and all(board[r][c + k] == checker for k in range(4)):
                return True
            # Check vertically
            if r <= rows - 4 and all(board[r + k][c] == checker for k in range(4)):
                return True
            # Check diagonal down-right
            if r <= rows - 4 and c <= cols - 4 and all(board[r + k][c + k] == checker for k in range(4)):
                return True
            # Check diagonal up-right
            if r >= 3 and c <= cols - 4 and all(board[r - k][c + k] == checker for k in range(4)):
                return True
    return False

def board_full(board):
    return all(cell != ' ' for cell in board[0])

# ==== MAIN ====

def main():
    board = create_board(ROWS, COLUMNS)
    current_player = random.randint(0, NUM_PLAYERS - 1)

    while True:
        clear_screen()
        print_board(board)
        checker = PLAYER_SYMBOLS[current_player]
        print(f"Player {checker}, please enter a column:")

        while True:
            user_input = input().strip()
            col_num = get_valid_column(board, user_input)

            if col_num == -1:
                print("Invalid input. Please enter a valid column label (e.g. A, B, ...).")
            elif col_num == -2:
                print("Column is full. You lose your turn!")
                col_num = None
                break
            else:
                break

        if col_num is not None:
            drop_checker(board, col_num, checker)
            if check_victory(board, checker):
                clear_screen()
                print_board(board)
                print(f"Player {checker} won!")
                break
            elif board_full(board):
                clear_screen()
                print_board(board)
                print("It's a draw!")
                break

        # Only skip turn if column was full
        if col_num is not None or col_num == -2:
            current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == '__main__':
    main()
