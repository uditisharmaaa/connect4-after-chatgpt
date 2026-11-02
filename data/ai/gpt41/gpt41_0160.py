import os
import random
import string

# --- Constants (for easy change of board size and number of players) ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2
PLAYER_TOKENS = ['X', 'O', 'V', 'H', 'M']
WIN_LENGTH = 4      # Number needed in a row to win

# --- Board functions ---

def create_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    os.system('clear')
    # Print column headers
    header = '  ' + '   '.join(string.ascii_uppercase[:len(board[0])])
    print(header)
    # Separator
    print('+' + '---+' * len(board[0]))
    # Rows
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+' + '---+' * len(board[0]))

def is_valid_column(col_input, cols):
    if len(col_input) != 1 or col_input not in string.ascii_uppercase[:cols]:
        return False
    return True

def get_lowest_empty_row(board, col):
    for row in reversed(range(len(board))):
        if board[row][col] == ' ':
            return row
    return None

def make_move(board, col, token):
    row = get_lowest_empty_row(board, col)
    if row is not None:
        board[row][col] = token
        return row, col
    return None

def is_board_full(board):
    for row in board:
        if ' ' in row:
            return False
    return True

# --- Win/Draw checking ---

def check_win(board, row, col, token):
    # Check all four directions: horizontal, vertical, two diagonals
    return (check_direction(board, row, col, token, 1, 0) or  # Horizontal
            check_direction(board, row, col, token, 0, 1) or  # Vertical
            check_direction(board, row, col, token, 1, 1) or  # Main Diagonal \
            check_direction(board, row, col, token, 1, -1))   # Anti Diagonal /

def check_direction(board, row, col, token, delta_row, delta_col):
    count = 1

    # Check in positive direction
    r, c = row + delta_row, col + delta_col
    while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == token:
        count += 1
        r += delta_row
        c += delta_col

    # Check in negative direction
    r, c = row - delta_row, col - delta_col
    while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == token:
        count += 1
        r -= delta_row
        c -= delta_col

    return count >= WIN_LENGTH

# --- Main Game Loop ---

def main():
    # Board and Players setup
    board = create_board(NUM_ROWS, NUM_COLS)
    tokens = PLAYER_TOKENS[:NUM_PLAYERS]
    # Randomly pick starting player
    current_player = random.randint(0, NUM_PLAYERS - 1)
    print_board(board)
    print(f"Randomly selected player {tokens[current_player]} will start.")
    input("Press Enter to start the game...")

    while True:
        print_board(board)
        print(f"Player {tokens[current_player]}, please enter a column:")

        col_input = input().strip().upper()
        # Input validation
        if not is_valid_column(col_input, NUM_COLS):
            print("Invalid input. Please enter a valid column letter (A-G) that exists on the board.")
            input("Press Enter to continue...")
            continue

        col = string.ascii_uppercase.index(col_input)

        row = get_lowest_empty_row(board, col)
        if row is None:
            print("Column is full! You lose your turn.")
            input("Press Enter to continue...")
            current_player = (current_player + 1) % NUM_PLAYERS
            continue

        # Place checker
        board[row][col] = tokens[current_player]

        # Check for win
        if check_win(board, row, col, tokens[current_player]):
            print_board(board)
            print(f"Player {tokens[current_player]} won!")
            break

        # Check for draw
        if is_board_full(board):
            print_board(board)
            print("It's a draw!")
            break

        # Next player's turn
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == '__main__':
    main()
