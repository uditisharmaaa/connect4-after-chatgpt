import os
import random
import string

# ---------------------- CONSTANTS ----------------------
NUM_ROWS = 6          # Number of rows (changeable - max 26 columns supported)
NUM_COLS = 7          # Number of columns
MAX_COLS = 26
NUM_PLAYERS = 2       # Changeable: between 2 and 5 ONLY (corresponding to checkers below)
PLAYER_CHECKERS = ['X', 'O', 'V', 'H', 'M']  # Valid up to 5 players

# ---------------------- FUNCTIONS ----------------------

def create_board(rows, cols):
    """Creates an empty board with the specified number of rows and columns."""
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Clears the screen and prints the current state of the board."""
    os.system('clear')
    cols = len(board[0])
    # Print column headers (A, B, C, ...)
    header = '  ' + '   '.join(string.ascii_uppercase[:cols])
    print(header)
    print('+' + '---+' * cols)
    for row in board:
        print('|' + '|'.join(' {} '.format(cell) for cell in row) + '|')
        print('+' + '---+' * cols)

def get_next_open_row(board, col):
    """Returns the next open row index in the specified column, or -1 if column is full."""
    for row in range(NUM_ROWS-1, -1, -1):
        if board[row][col] == " ":
            return row
    return -1

def is_valid_column(col_input, board):
    """Check if the input is a valid column to place a checker."""
    if len(col_input) != 1 or not col_input.isalpha():
        return False
    col_letter = col_input.upper()
    cols = len(board[0])
    if col_letter < 'A' or col_letter >= chr(ord('A')+cols):
        return False
    col_idx = ord(col_letter) - ord('A')
    if board[0][col_idx] != " ":
        return False
    return True

def check_win(board, row, col, checker):
    """Checks if placing the checker at (row, col) wins the game."""
    def count_consecutive(dx, dy):
        count = 0
        r, c = row + dx, col + dy
        while 0 <= r < NUM_ROWS and 0 <= c < NUM_COLS and board[r][c] == checker:
            count += 1
            r += dx
            c += dy
        return count

    directions = [ (0,1), (1,0), (1,1), (1,-1) ]  # H, V, diagonal down-right, diagonal down-left
    for dx, dy in directions:
        total = 1
        total += count_consecutive(dx, dy)
        total += count_consecutive(-dx, -dy)
        if total >= 4:
            return True
    return False

def board_full(board):
    """Returns True if the board is full, False otherwise."""
    return all(cell != " " for cell in board[0])

def select_start_player(num_players):
    """Randomly selects a starting player."""
    return random.randint(0, num_players-1)

def get_player_input(player_checker, board):
    """Requests and validates the move from the player."""
    while True:
        col_input = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        if (len(col_input)==1 and col_input.isalpha()):
            col_num = ord(col_input) - ord('A')
            if 0 <= col_num < len(board[0]):
                if board[0][col_num] == " ":
                    return col_num
                else:
                    print("That column is full. Try another column.")
            else:
                print("Invalid column letter. Please enter a valid column (A-{}).".format(string.ascii_uppercase[len(board[0])-1]))
        else:
            print("Invalid input. Please enter a single column letter (A-{}).".format(string.ascii_uppercase[len(board[0])-1]))

# ---------------------- MAIN GAME LOGIC ----------------------

def main():
    # Limit dimensions and player count for assignment purpose
    rows = NUM_ROWS
    cols = NUM_COLS
    if NUM_PLAYERS < 2 or NUM_PLAYERS > 5 or cols < 1 or cols > MAX_COLS:
        print("ERROR: Invalid player count or column dimensions")
        return

    checkers = PLAYER_CHECKERS[:NUM_PLAYERS]
    board = create_board(rows, cols)
    current_player = select_start_player(NUM_PLAYERS)

    print_board(board)
    print(f"Player {checkers[current_player]} starts!\n")

    while True:
        player_checker = checkers[current_player]
        col = get_player_input(player_checker, board)

        row = get_next_open_row(board, col)
        if row == -1:
            # Column FULL, lose turn!
            print(f"Column {string.ascii_uppercase[col]} is full! You lose your turn.")
            current_player = (current_player + 1) % NUM_PLAYERS
            print_board(board)
            continue

        # Place the checker
        board[row][col] = player_checker
        print_board(board)

        # Check for a winner
        if check_win(board, row, col, player_checker):
            print(f"Player {player_checker} won!")
            return

        # Check draw
        if board_full(board):
            print("It's a draw. No more spaces left!")
            return

        # Next player's turn
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
