import os
import random
import sys

# ----------------------- CONSTANT VARIABLES -----------------------
NUM_ROWS = 6            # Board rows
NUM_COLS = 7            # Board columns (max 26)
PLAYER_CHECKERS = ['X', 'O', 'V', 'H', 'M']  # Supported player checkers
NUM_PLAYERS = 2         # Changeable from 2 to 5
WIN_LENGTH = 4          # Number in row to win

# -------------------- BOARD CREATION AND PRINTING -----------------
def create_board(rows, cols):
    """Create the game board initialized with spaces."""
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Clear the screen and print the game board."""
    os.system('clear')
    column_labels = [chr(ord('A') + c) for c in range(len(board[0]))]
    # Print column labels
    print('  ' + '   '.join(column_labels))
    # Print top border
    print('+' + '---+' * len(board[0]))
    # Print board rows
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+' + '---+' * len(board[0]))

# --------------------- GAME FUNCTIONS -----------------------

def is_valid_column(input_col, board):
    """Check if column input is valid and not full."""
    if len(input_col) != 1 or not input_col.isalpha():
        return False
    col = ord(input_col) - ord('A')
    if col < 0 or col >= len(board[0]):
        return False
    if board[0][col] != ' ':
        return False
    return True

def get_next_open_row(board, col):
    """Return the lowest empty row index in a given column. If full, return None."""
    for row in range(len(board)-1, -1, -1):
        if board[row][col] == ' ':
            return row
    return None

def drop_checker(board, row, col, checker):
    """Place player's checker in the cell."""
    board[row][col] = checker

def is_board_full(board):
    """Check if the board is full."""
    for row in board:
        if ' ' in row:
            return False
    return True

def check_win(board, checker):
    """Check horizontal, vertical, diagonal (both ways) win for the player."""
    rows = len(board)
    cols = len(board[0])
    # Horizontal check
    for r in range(rows):
        for c in range(cols - WIN_LENGTH + 1):
            if all(board[r][c + i] == checker for i in range(WIN_LENGTH)):
                return True
    # Vertical check
    for c in range(cols):
        for r in range(rows - WIN_LENGTH + 1):
            if all(board[r + i][c] == checker for i in range(WIN_LENGTH)):
                return True
    # Diagonal down-right (\)
    for r in range(rows - WIN_LENGTH + 1):
        for c in range(cols - WIN_LENGTH + 1):
            if all(board[r + i][c + i] == checker for i in range(WIN_LENGTH)):
                return True
    # Diagonal up-right (/)
    for r in range(WIN_LENGTH - 1, rows):
        for c in range(cols - WIN_LENGTH + 1):
            if all(board[r - i][c + i] == checker for i in range(WIN_LENGTH)):
                return True
    return False

# ------------------------- MAIN GAME LOOP ------------------------
def main():
    # Set up
    board = create_board(NUM_ROWS, NUM_COLS)
    checkers = PLAYER_CHECKERS[:NUM_PLAYERS]
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)
    print_board(board)
    print(f"Player {checkers[current_player_idx]} goes first!")
    input("Press Enter to start...")

    while True:
        print_board(board)
        player_checker = checkers[current_player_idx]
        valid_move = False
        while not valid_move:
            move = input(f"Player {player_checker}, please enter a column: ").strip().upper()
            if not is_valid_column(move, board):
                print("Invalid column! Please enter a valid column letter with available space.")
                continue
            col = ord(move) - ord('A')
            row = get_next_open_row(board, col)
            if row is not None:
                drop_checker(board, row, col, player_checker)
                valid_move = True
            else:
                print("Column full! You lose your turn.")
                valid_move = True  # lose the turn (do not get another try)

        # Check for win
        if check_win(board, player_checker):
            print_board(board)
            print(f"Player {player_checker} won!")
            break
        # Check for draw
        if is_board_full(board):
            print_board(board)
            print("The game is a draw!")
            break
        # Next player's turn
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

if __name__ == '__main__':
    main()
