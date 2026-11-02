import os
import random
import string

# Constants (for submission: 6 rows x 7 columns, 2 players)
ROWS = 6
COLUMNS = 7
PLAYERS_COUNT = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']
WIN_LENGTH = 4

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    # Print column headers A, B, C...
    header = "  " + "   ".join(string.ascii_uppercase[:len(board[0])])
    print(header)
    # Print separator line
    sep = "+" + "---+" * len(board[0])
    for row in board:
        print(sep)
        print('|' + '|'.join(f" {cell} " for cell in row) + '|')
    print(sep)

def is_valid_column(column, board):
    # Check if column is in range and column not full
    if column not in string.ascii_uppercase[:len(board[0])]:
        return False
    col_idx = string.ascii_uppercase.index(column)
    # Column full if top row is occupied
    return board[0][col_idx] == ' '

def drop_checker(board, col, checker):
    # col is column letter, drop checker in the lowest free cell
    col_idx = string.ascii_uppercase.index(col)
    for row_idx in reversed(range(len(board))):
        if board[row_idx][col_idx] == ' ':
            board[row_idx][col_idx] = checker
            return row_idx, col_idx  # return position where checker was placed
    return None  # Column full (should not happen if checked before)

def input_column(player, board):
    while True:
        col = input(f"Player {player}, please enter a column: ").strip().upper()
        if len(col) != 1 or col not in string.ascii_uppercase[:len(board[0])]:
            # Invalid char or multichar input
            continue
        if not is_valid_column(col, board):
            # Column full, lose turn as per instructions
            # Inform player and return None
            print(f"Column {col} is full. Player {player} loses the turn.")
            return None
        return col

def check_direction(board, start_row, start_col, delta_row, delta_col, checker):
    count = 0
    row, col = start_row, start_col
    max_row = len(board)
    max_col = len(board[0])
    while 0 <= row < max_row and 0 <= col < max_col:
        if board[row][col] == checker:
            count += 1
            if count == WIN_LENGTH:
                return True
        else:
            count = 0
        row += delta_row
        col += delta_col
    return False

def check_win(board, row, col, checker):
    # Only need to check directions passing through (row, col)
    directions = [
        (0, 1),   # Horizontal right
        (1, 0),   # Vertical down
        (1, 1),   # Diagonal down-right
        (1, -1),  # Diagonal down-left
    ]
    for dr, dc in directions:
        # To cover entire line that could contain 4 in a row that includes (row,col),
        # we must check backward and forward along this direction
        count = 1  # counting the position itself
        # check backward
        r, c = row - dr, col - dc
        while 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        # check forward
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        if count >= WIN_LENGTH:
            return True
    return False

def board_full(board):
    # If no space in the top row means board full
    return all(cell != ' ' for cell in board[0])

def main():
    board = create_board(ROWS, COLUMNS)
    players = CHECKERS[:PLAYERS_COUNT]
    # Randomly pick the first player index
    current_player_idx = random.randint(0, PLAYERS_COUNT - 1)
    print_board(board)
    # Notify who goes first
    print(f"Player {players[current_player_idx]} starts the game.")
    while True:
        checker = players[current_player_idx]
        col = input_column(checker, board)
        if col is None:
            # Player loses turn because full column
            current_player_idx = (current_player_idx + 1) % PLAYERS_COUNT
            print_board(board)
            continue
        placement = drop_checker(board, col, checker)
        print_board(board)
        if placement is None:
            # Should not happen since input_column guards against full columns
            current_player_idx = (current_player_idx + 1) % PLAYERS_COUNT
            continue
        row, col_idx = placement
        if check_win(board, row, col_idx, checker):
            print(f"Player {checker} won!")
            break
        if board_full(board):
            print("The game is a draw!")
            break
        current_player_idx = (current_player_idx + 1) % PLAYERS_COUNT

if __name__ == "__main__":
    main()
