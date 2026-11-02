import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYER_COUNT = 2
PLAYERS = ['X', 'O', 'V', 'H', 'M']  # Max 5 players, use only first PLAYER_COUNT
WIN_LENGTH = 4

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    cols = len(board[0])
    header = '  ' + '   '.join([chr(ord('A') + i) for i in range(cols)])
    line = '+' + '---+' * cols
    print(header)
    for r in range(len(board)):
        print(line)
        row_str = '| ' + ' | '.join(board[r]) + ' |'
        print(row_str)
    print(line)

def column_to_index(col_char):
    col_char = col_char.upper()
    if 'A' <= col_char <= chr(ord('A') + COLUMNS - 1):
        return ord(col_char) - ord('A')
    return -1

def is_column_full(board, col_idx):
    return board[0][col_idx] != ' '

def place_checker(board, col_idx, checker):
    # place checker in lowest available cell in the column
    for row in reversed(range(len(board))):
        if board[row][col_idx] == ' ':
            board[row][col_idx] = checker
            return row, col_idx
    return -1, -1  # full column, no place to put

def is_valid_input(input_str, board):
    if len(input_str) != 1:
        return False
    col_idx = column_to_index(input_str)
    if col_idx == -1:
        return False
    if is_column_full(board, col_idx):
        return False
    return True

def check_winner(board, last_row, last_col, checker):
    directions = [
        (0, 1),   # horizontal right
        (1, 0),   # vertical down
        (1, 1),   # diagonal down-right
        (1, -1)   # diagonal down-left
    ]
    rows = len(board)
    cols = len(board[0])

    for dr, dc in directions:
        count = 1
        # check in positive direction
        r, c = last_row + dr, last_col + dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # check in negative direction
        r, c = last_row - dr, last_col - dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        if count >= WIN_LENGTH:
            return True
    return False

def board_full(board):
    for c in range(len(board[0])):
        if not is_column_full(board, c):
            return False
    return True

def main():
    board = create_board(ROWS, COLUMNS)
    players = PLAYERS[:PLAYER_COUNT]
    current_player_idx = random.randint(0, PLAYER_COUNT - 1)

    while True:
        clear_screen()
        print_board(board)
        current_checker = players[current_player_idx]
        prompt = f"Player {current_checker}, please enter a column: "
        while True:
            col_input = input(prompt).strip()
            if not is_valid_input(col_input, board):
                # Special case: if column is full => lose turn (no repeat prompt)
                col_idx = column_to_index(col_input)
                if 0 <= col_idx < COLUMNS and is_column_full(board, col_idx):
                    # lose turn:
                    break
                # Otherwise invalid input => ask again
                continue
            else:
                col_idx = column_to_index(col_input)
                break

        # if invalid input caused lost turn:
        if col_idx == -1 or is_column_full(board, col_idx):
            # skip turn
            current_player_idx = (current_player_idx + 1) % PLAYER_COUNT
            continue

        row, col = place_checker(board, col_idx, current_checker)
        if row == -1:
            # This should not happen due to checks above but just in case
            current_player_idx = (current_player_idx + 1) % PLAYER_COUNT
            continue

        if check_winner(board, row, col, current_checker):
            clear_screen()
            print_board(board)
            print(f"Player {current_checker} won!")
            break

        if board_full(board):
            clear_screen()
            print_board(board)
            print("The game is a draw!")
            break

        current_player_idx = (current_player_idx + 1) % PLAYER_COUNT

if __name__ == '__main__':
    main()
