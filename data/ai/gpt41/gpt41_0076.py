import os
import random
import string

# Constants
ROWS = 6
COLS = 7
MAX_COLS = 26
NUM_PLAYERS = 2  # Can be 2-5

PLAYER_CHECKERS = ['X', 'O', 'V', 'H', 'M']

def clear_screen():
    os.system('clear')  # For UNIX/Linux/Mac. For Windows, use 'cls'.

def create_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    cols = len(board[0])
    # Print column labels
    col_labels = '  ' + '   '.join(string.ascii_uppercase[:cols])
    print(col_labels)
    print('+' + '---+' * cols)
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+' + '---+' * cols)

def get_valid_columns(board):
    return [i for i in range(len(board[0])) if board[0][i] == ' ']

def input_column(current_player, board):
    valid_cols = get_valid_columns(board)
    cols = len(board[0])
    valid_letters = [string.ascii_uppercase[i] for i in valid_cols]
    while True:
        col_input = input(f"Player {current_player}, please enter a column: ").strip().upper()
        if len(col_input) != 1 or col_input not in string.ascii_uppercase[:cols]:
            print("Invalid input. Please enter a valid column letter.")
            continue
        col_idx = string.ascii_uppercase.index(col_input)
        if col_idx >= cols:
            print("Invalid column. Please select a valid column.")
            continue
        if col_idx not in valid_cols:
            print("Column is full. You lose your turn.")
            return None  # Return None if column is full
        return col_idx

def drop_checker(board, col, checker):
    for row in reversed(range(len(board))):
        if board[row][col] == ' ':
            board[row][col] = checker
            return row, col

def check_win(board, row, col, checker):
    return (check_direction(board, row, col, checker, 1, 0) or  # Vertical
            check_direction(board, row, col, checker, 0, 1) or  # Horizontal
            check_direction(board, row, col, checker, 1, 1) or  # Diagonal /
            check_direction(board, row, col, checker, 1, -1))   # Diagonal \

def check_direction(board, row, col, checker, d_row, d_col):
    count = 1
    # Check in the positive direction
    count += count_checkers(board, row, col, checker, d_row, d_col)
    # Check in the negative direction
    count += count_checkers(board, row, col, checker, -d_row, -d_col)
    return count >= 4

def count_checkers(board, row, col, checker, d_row, d_col):
    rows, cols = len(board), len(board[0])
    count = 0
    r, c = row + d_row, col + d_col
    while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
        count += 1
        r += d_row
        c += d_col
    return count

def check_draw(board):
    return all(cell != ' ' for cell in board[0])  # If top row is full, draw.

def main():
    board = create_board(ROWS, COLS)
    checkers = PLAYER_CHECKERS[:NUM_PLAYERS]
    players = list(range(NUM_PLAYERS))
    start_player = random.choice(players)
    current_player = start_player
    clear_screen()
    print_board(board)
    winner = None

    while True:
        checker = checkers[current_player]
        valid_cols = get_valid_columns(board)
        if not valid_cols:
            print("It's a draw!")
            break

        col = input_column(checker, board)
        clear_screen()
        if col is None:
            print_board(board)
            # Player loses turn if column is full
            current_player = (current_player + 1) % NUM_PLAYERS
            continue

        row, col_pos = drop_checker(board, col, checker)
        print_board(board)

        if check_win(board, row, col_pos, checker):
            print(f"Player {checker} won!")
            break
        elif check_draw(board):
            print("It's a draw!")
            break

        # Next player's turn
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == '__main__':
    main()
