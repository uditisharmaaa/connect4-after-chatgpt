import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']
WIN_LENGTH = 4
COLUMN_LABELS = [chr(ord('A') + i) for i in range(COLS)]

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    # Print column headers
    print('  ' + '   '.join(COLUMN_LABELS))
    print('+' + '---+' * len(board[0]))
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+' + '---+' * len(board[0]))

def is_valid_column(col_letter):
    return col_letter in COLUMN_LABELS

def get_column_index(col_letter):
    return COLUMN_LABELS.index(col_letter)

def column_full(board, col):
    return board[0][col] != ' '

def place_checker(board, col, checker):
    # Place checker at lowest available row in column
    for row_idx in range(len(board)-1, -1, -1):
        if board[row_idx][col] == ' ':
            board[row_idx][col] = checker
            return row_idx, col
    # If column is full (should not happen if checked before)
    return None

def check_direction(board, start_row, start_col, delta_row, delta_col, checker):
    count = 0
    row, col = start_row, start_col
    while 0 <= row < ROWS and 0 <= col < COLS and board[row][col] == checker:
        count += 1
        row += delta_row
        col += delta_col
    return count

def check_win(board, row, col, checker):
    # Check all directions from the placed checker for WIN_LENGTH in a row
    directions = [
        (0, 1),  # horizontal right
        (1, 0),  # vertical down
        (1, 1),  # diagonal down-right
        (1, -1)  # diagonal down-left
    ]
    for dr, dc in directions:
        # count consecutive same checkers in both directions
        count = 1  # count the placed checker itself
        count += count_consecutive(board, row, col, dr, dc, checker)
        count += count_consecutive(board, row, col, -dr, -dc, checker)
        if count >= WIN_LENGTH:
            return True
    return False

def count_consecutive(board, start_row, start_col, delta_row, delta_col, checker):
    count = 0
    row = start_row + delta_row
    col = start_col + delta_col
    while 0 <= row < ROWS and 0 <= col < COLS and board[row][col] == checker:
        count += 1
        row += delta_row
        col += delta_col
    return count

def board_full(board):
    return all(board[0][col] != ' ' for col in range(COLS))

def get_valid_input(player_checker):
    while True:
        inp = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        if not inp or len(inp) != 1:
            print("Invalid input. Enter a single column letter (A-G).")
            continue
        if not is_valid_column(inp):
            print(f"Invalid column. Choose from {', '.join(COLUMN_LABELS)}.")
            continue
        col_idx = get_column_index(inp)
        if column_full(board, col_idx):
            print(f"Column {inp} is full. You lose your turn.")
            return None  # lose turn
        return col_idx

def main():
    global board
    board = create_board(ROWS, COLS)
    players = CHECKERS[:NUM_PLAYERS]
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)
    print_board(board)

    while True:
        player_checker = players[current_player_idx]
        col = get_valid_input(player_checker)
        if col is None:
            # lost turn because column was full
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            print_board(board)
            continue
        placement = place_checker(board, col, player_checker)
        print_board(board)

        if placement is None:
            # Defensive, should not happen here because we validated input
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            continue

        row_placed, col_placed = placement

        if check_win(board, row_placed, col_placed, player_checker):
            print(f"Player {player_checker} won!")
            break

        if board_full(board):
            print("The game is a draw!")
            break

        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
