import os
import random
import sys
import string

# === Global Constants ===
NUM_ROWS = 6
NUM_COLS = 7   # up to 26
NUM_PLAYERS = 2  # between 2 and 5
CHECKERS = ['X', 'O', 'V', 'H', 'M']  # Max 5, order matters

# For supporting up to 26 columns
COLUMN_LABELS = [chr(ord('A') + i) for i in range(NUM_COLS)]

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')

def create_board(rows, cols):
    """Creates and returns an empty board with the given dimensions."""
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Prints the board in the formatted style."""
    clear_screen()
    # Print column labels
    print('  ' + '   '.join(COLUMN_LABELS[:len(board[0])]))
    # Print top border
    print('+' + '---+' * len(board[0]))
    # Print rows
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+' + '---+' * len(board[0]))

def get_player_input(board, player_checker):
    """Prompts the player for valid input and returns the selected column index."""
    while True:
        user_input = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        if len(user_input) != 1 or user_input not in COLUMN_LABELS[:len(board[0])]:
            print("Invalid input! Please enter a valid column letter (e.g., A, B, ...).")
            continue
        col = COLUMN_LABELS.index(user_input)
        # Check if the column is not full
        if board[0][col] != ' ':
            print("That column is full! Please choose another one.")
            return None  # Lose the turn
        return col

def place_checker(board, col, checker):
    """Places the player's checker in the chosen column."""
    # Place from bottom up
    for row in reversed(range(len(board))):
        if board[row][col] == ' ':
            board[row][col] = checker
            return row, col  # Return the position for win checking
    return None  # should not happen if input is validated

def is_board_full(board):
    """Checks if the board is full."""
    return all(board[0][col] != ' ' for col in range(len(board[0])))

def check_win(board, checker):
    """Checks for a win of 'checker' in the board (horiz, vert, or diagonal)."""
    rows = len(board)
    cols = len(board[0])
    # Check horizontal
    for r in range(rows):
        for c in range(cols - 3):
            if all(board[r][c+i] == checker for i in range(4)):
                return True
    # Check vertical
    for c in range(cols):
        for r in range(rows - 3):
            if all(board[r+i][c] == checker for i in range(4)):
                return True
    # Check main diagonal (\)
    for r in range(rows - 3):
        for c in range(cols - 3):
            if all(board[r+i][c+i] == checker for i in range(4)):
                return True
    # Check anti-diagonal (/)
    for r in range(3, rows):
        for c in range(cols - 3):
            if all(board[r-i][c+i] == checker for i in range(4)):
                return True
    return False

def main():
    # Set up board and players
    if NUM_COLS > 26 or NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
        print('Error: Invalid board dimensions or number of players.')
        sys.exit(1)
    board = create_board(NUM_ROWS, NUM_COLS)
    player_checkers = CHECKERS[:NUM_PLAYERS]
    # Random starting player
    current_player = random.randint(0, NUM_PLAYERS - 1)

    print_board(board)

    # Game loop
    while True:
        player_checker = player_checkers[current_player]
        col = get_player_input(board, player_checker)
        if col is not None:
            pos = place_checker(board, col, player_checker)
            print_board(board)
            # Check for win
            if check_win(board, player_checker):
                print(f'Player {player_checker} won!')
                break
            elif is_board_full(board):
                print('The game is a draw!')
                break
            # Next player's turn
        else:
            print(f"Turn skipped: Player {player_checker} loses the turn as column is full.")
            input('Press Enter to continue...')
            print_board(board)
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == '__main__':
    main()
