import os
import random

# Constants
ROWS = 6
COLS = 7
MAX_PLAYERS = 5
NUM_PLAYERS = 2  # Set to 2 for submission
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def clear_screen():
    os.system('clear')

def create_board(rows=ROWS, cols=COLS):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    cols = len(board[0])
    # Print column labels
    labels = [chr(ord('A') + i) for i in range(cols)]
    print('  ' + '   '.join(labels))
    # Print the board rows and borders
    horizontal_line = '+' + '---+' * cols
    for r in range(len(board)):
        print(horizontal_line)
        row_str = '| ' + ' | '.join(board[r]) + ' |'
        print(row_str)
    print(horizontal_line)

def valid_column(col_letter, cols=COLS):
    if len(col_letter) != 1:
        return False
    if not 'A' <= col_letter <= chr(ord('A') + cols -1):
        return False
    return True

def column_index(col_letter):
    return ord(col_letter) - ord('A')

def place_checker(board, col_idx, checker):
    # Place checker in lowest available space of column
    for row in reversed(range(len(board))):
        if board[row][col_idx] == ' ':
            board[row][col_idx] = checker
            return row, col_idx
    return None  # Column full

def check_win(board, row, col, checker):
    rows = len(board)
    cols = len(board[0])

    def count_direction(delta_r, delta_c):
        count = 0
        r, c = row + delta_r, col + delta_c
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r += delta_r
            c += delta_c
        return count

    # Check all 4 directions: horizontal, vertical, diag1 (/), diag2 (\)
    # Total count includes current checker + count in both directions
    directions = [ (0,1), (1,0), (1,1), (1,-1) ]
    for dr, dc in directions:
        count = 1  # current checker
        count += count_direction(dr, dc)
        count += count_direction(-dr, -dc)
        if count >= 4:
            return True
    return False

def board_full(board):
    for c in range(len(board[0])):
        if board[0][c] == ' ':
            return False
    return True

def main():
    board = create_board()
    cols = len(board[0])
    players = CHECKERS[:NUM_PLAYERS]

    current_player_idx = random.randint(0, NUM_PLAYERS -1)

    print_board(board)

    while True:
        checker = players[current_player_idx]
        print(f"Player {checker}, please enter a column:")
        col_input = input().strip().upper()
        if not valid_column(col_input, cols):
            # invalid input, ask again
            continue
        col_i = column_index(col_input)
        placed = place_checker(board, col_i, checker)
        if placed is None:
            # column full, lose turn
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            print_board(board)
            continue

        print_board(board)
        r, c = placed
        # Check win
        if check_win(board, r, c, checker):
            print(f"Player {checker} won!")
            break
        # Check draw
        if board_full(board):
            print("The game is a draw!")
            break
        # Next player
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
