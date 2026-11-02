import os
import random
import string

# =========================
# CONSTANTS
# =========================
ROWS = 6                # Number of rows
COLUMNS = 7             # Number of columns (max 26, labeled A-Z)
NUM_PLAYERS = 2         # Number of players (from 2 to 5)
WIN_COUNT = 4           # Number in a row to win

CHECKERS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]
COLUMN_LABELS = list(string.ascii_uppercase)[:COLUMNS]

# =========================
# UTILITIES
# =========================
def clear_screen():
    os.system('clear')

def print_board(board):
    clear_screen()
    # Print column letters
    label_line = '  ' + '   '.join(COLUMN_LABELS)
    print(label_line)
    print('+' + '---+' * COLUMNS)
    for row in board:
        print('| ' + ' | '.join(row) + ' |')
        print('+' + '---+' * COLUMNS)

# =========================
# BOARD INITIALIZATION
# =========================
def create_board():
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

# =========================
# INPUT VALIDATION
# =========================
def valid_column_input(col_input):
    if len(col_input) != 1:
        return False
    if col_input not in COLUMN_LABELS:
        return False
    return True

def is_column_full(board, col_idx):
    return all(board[row][col_idx] != ' ' for row in range(ROWS))

# =========================
# GAME LOGIC FUNCTIONS
# =========================
def drop_checker(board, col_idx, checker):
    for row in reversed(range(ROWS)):
        if board[row][col_idx] == ' ':
            board[row][col_idx] = checker
            return row
    return None  # Shouldn't get here if checked correctly

def is_board_full(board):
    return all(cell != ' ' for row in board for cell in row)

def check_direction(board, row, col, d_row, d_col, checker):
    count = 0
    r, c = row, col
    while 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == checker:
        count += 1
        r += d_row
        c += d_col
    return count

def check_win(board, row, col, checker):
    # Horizontal
    left = check_direction(board, row, col - 1, 0, -1, checker)
    right = check_direction(board, row, col + 1, 0, 1, checker)
    if (1 + left + right) >= WIN_COUNT:
        return True
    # Vertical
    down = check_direction(board, row + 1, col, 1, 0, checker)
    up = check_direction(board, row - 1, col, -1, 0, checker)
    if (1 + down + up) >= WIN_COUNT:
        return True
    # Diagonal /
    up_right = check_direction(board, row - 1, col + 1, -1, 1, checker)
    down_left = check_direction(board, row + 1, col - 1, 1, -1, checker)
    if (1 + up_right + down_left) >= WIN_COUNT:
        return True
    # Diagonal \
    up_left = check_direction(board, row - 1, col - 1, -1, -1, checker)
    down_right = check_direction(board, row + 1, col + 1, 1, 1, checker)
    if (1 + up_left + down_right) >= WIN_COUNT:
        return True
    return False

# =========================
# MAIN GAME LOOP
# =========================
def main():
    board = create_board()
    players = [{'name': f'Player {CHECKERS[i]}', 'checker': CHECKERS[i]} for i in range(NUM_PLAYERS)]
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)
    print_board(board)
    print(f'{players[current_player_idx]["name"]} ({players[current_player_idx]["checker"]}) randomly selected to start.')
    input("Press Enter to start the game...")
    
    game_over = False

    while not game_over:
        print_board(board)
        player = players[current_player_idx]
        checker = player['checker']

        while True:
            col_input = input(f"{player['name']} ({checker}), please enter a column: ").strip().upper()
            # Input validation
            if not valid_column_input(col_input):
                print("Invalid input. Please enter a single letter corresponding to a valid column (A-G, etc).")
                continue
            col_idx = COLUMN_LABELS.index(col_input)
            if is_column_full(board, col_idx):
                print("This column is full. You lose your turn.")
                break  # Lose turn if full
            # Place checker
            row_idx = drop_checker(board, col_idx, checker)
            # Win check
            if check_win(board, row_idx, col_idx, checker):
                print_board(board)
                print(f"{player['name']} won!")
                game_over = True
                break
            # Draw check
            if is_board_full(board):
                print_board(board)
                print("The game is a draw!")
                game_over = True
                break
            # Next player
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            break  # Only breaks if successful drop or lost turn

if __name__ == '__main__':
    main()
