import os
import random
import string

# ----- Constants -----
ROWS = 6                    # Number of rows (can change, but default is 6)
COLUMNS = 7                 # Number of columns (can change, but default is 7, max 26)
NUM_PLAYERS = 2             # Number of players (can set between 2 and 5, default 2)
PLAYER_CHECKERS = ['X', 'O', 'V', 'H', 'M']  # Checkers for up to 5 players
COLUMN_LABELS = string.ascii_uppercase[:COLUMNS]

# ----- Functions -----

def clear_screen():
    '''Clears the terminal screen.'''
    os.system('clear')


def create_board():
    '''Creates a new game board with the current ROWS and COLUMNS constants.'''
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]


def print_board(board):
    '''Prints the game board in a formatted style with column labels.'''
    clear_screen()
    # Print column labels
    print('  ' + '   '.join(COLUMN_LABELS))
    print('+' + '---+' * COLUMNS)
    # Print board rows
    for row in board:
        print('|' + '|'.join(' {} '.format(cell) for cell in row) + '|')
        print('+' + '---+' * COLUMNS)


def get_valid_column_input(board, player_checker):
    '''
    Prompts the current player for a valid column letter and
    validates the input. Returns the column index or None if the column is full.
    '''
    while True:
        user_input = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        if len(user_input) != 1:
            print("Invalid input. Enter only one column letter.")
            continue
        if user_input not in COLUMN_LABELS:
            print("Invalid column. Enter a valid column letter.")
            continue
        col_idx = COLUMN_LABELS.index(user_input)
        # If column is full
        if board[0][col_idx] != ' ':
            print("Column is full! You lose your turn.")
            return None  # Player loses the turn as per assignment
        return col_idx


def place_checker(board, col_idx, player_checker):
    '''
    Places the player's checker in the lowest available
    row in the selected column. Returns the row index where placed, or None if full.
    '''
    for row in reversed(range(ROWS)):
        if board[row][col_idx] == ' ':
            board[row][col_idx] = player_checker
            return row
    return None


def check_win(board, player_checker, last_row, last_col):
    '''
    Checks for a win from the newest checker placed (for performance).
    Returns True if player wins.
    '''
    def count_direction(d_row, d_col):
        count = 0
        row, col = last_row + d_row, last_col + d_col
        while 0 <= row < ROWS and 0 <= col < COLUMNS and board[row][col] == player_checker:
            count += 1
            row += d_row
            col += d_col
        return count

    # Directions: (vertical, horizontal, diag /, diag \)
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
    for d_row, d_col in directions:
        count = 1  # Count the last placed piece itself
        count += count_direction(d_row, d_col)
        count += count_direction(-d_row, -d_col)
        if count >= 4:
            return True
    return False


def is_board_full(board):
    '''Returns True if the board is completely filled.'''
    for cell in board[0]:
        if cell == ' ':
            return False
    return True


def main():
    # Board and player initialization
    board = create_board()
    current_player = random.randint(0, NUM_PLAYERS - 1)  # Randomly select starting player
    players = PLAYER_CHECKERS[:NUM_PLAYERS]
    print_board(board)
    print(f"Player {players[current_player]} starts!\n")

    while True:
        print_board(board)
        col_idx = get_valid_column_input(board, players[current_player])
        if col_idx is None:
            # Player loses the turn if column is full
            current_player = (current_player + 1) % NUM_PLAYERS
            continue

        row_idx = place_checker(board, col_idx, players[current_player])

        # Check for win: only need to check relative to last move
        if check_win(board, players[current_player], row_idx, col_idx):
            print_board(board)
            print(f"Player {players[current_player]} won!")
            break
        elif is_board_full(board):
            print_board(board)
            print("It's a draw!")
            break

        # Next player's turn
        current_player = (current_player + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
