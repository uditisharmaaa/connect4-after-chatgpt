import os
import random
import string

# Constants
ROWS = 6
COLUMNS = 7
MAX_COLUMNS = 26
MIN_PLAYERS = 2
MAX_PLAYERS = 5
NUM_PLAYERS = 2  # Set to 2 for submission, can be changed to test

CHECKERS = ['X', 'O', 'V', 'H', 'M']

# Create board
def create_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

# Print board
def print_board(board, checkers):
    os.system('clear')    # Clear the terminal screen
    letters = string.ascii_uppercase[:len(board[0])]
    print('\n  ' + '   '.join(letters))
    print('+' + '---+' * len(board[0]))
    for row in board:
        print('|' + '|'.join(' {0} '.format(cell) for cell in row) + '|')
        print('+' + '---+' * len(board[0]))

# Choose random first player
def choose_first_player(num_players):
    return random.randint(0, num_players - 1)

# Check if move is valid (input)
def is_valid_column(col_str, num_cols):
    if len(col_str) != 1 or col_str not in string.ascii_uppercase[:num_cols]:
        return False
    return True

# Make move: returns row index where checker is placed, or None if column full
def make_move(board, col, checker):
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == ' ':
            board[r][col] = checker
            return r
    return None  # Column full

# Check for win: horizontal, vertical, diagonal \ and diagonal /
def check_win(board, last_row, last_col, checker):
    directions = [ (0,1), (1,0), (1,1), (1,-1) ]  # right, down, diag \, diag /
    for dr, dc in directions:
        count = 1  # current checker
        # check one direction
        r, c = last_row + dr, last_col + dc
        while 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # check opposite direction
        r, c = last_row - dr, last_col - dc
        while 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        if count >= 4:
            return True
    return False

# Check for draw
def check_draw(board):
    for row in board:
        if ' ' in row:
            return False
    return True

def main():
    # Setup
    board = create_board(ROWS, COLUMNS)
    players = [CHECKERS[i] for i in range(NUM_PLAYERS)]
    current = choose_first_player(NUM_PLAYERS)
    last_move = (-1, -1)

    print_board(board, players)
    print(f"Player {players[current]} will start!")

    while True:
        print_board(board, players)
        col_input = input(f'Player {players[current]}, please enter a column: ').strip().upper()
        # Validate input
        while not is_valid_column(col_input, COLUMNS):
            print("Invalid input. Please enter a valid column letter (A-{0}).".format(string.ascii_uppercase[COLUMNS-1]))
            col_input = input(f'Player {players[current]}, please enter a column: ').strip().upper()
        col_num = string.ascii_uppercase.index(col_input)
        row_num = make_move(board, col_num, players[current])
        if row_num is None:    # Column is full, turn is lost
            print_board(board, players)
            print(f"Column {col_input} is full. Player {players[current]} loses the turn.")
            current = (current + 1) % NUM_PLAYERS
            continue
        # Check for win
        if check_win(board, row_num, col_num, players[current]):
            print_board(board, players)
            print(f"Player {players[current]} won!")
            break
        # Check for draw
        if check_draw(board):
            print_board(board, players)
            print("Game ended in a draw!")
            break
        # Next player
        current = (current + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
