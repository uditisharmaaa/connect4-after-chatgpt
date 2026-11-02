import os
import random
import string

# Constants
ROWS = 6
COLS = 7
MAX_COLS = 26
NUM_PLAYERS = 2       # For submission, should be between 2 and 5
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    """Initializes the board with whitespaces."""
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Prints the board to the terminal as specified."""
    cols = len(board[0])
    # Print column labels
    col_labels = ' '.join(['  ' + string.ascii_uppercase[i] + ' ' for i in range(cols)])
    print(col_labels)
    # Print top border
    print('+' + '---+' * cols)
    for row in board:
        print('|' + '|'.join(' {} '.format(cell) for cell in row) + '|')
        print('+' + '---+' * cols)

def get_valid_columns(board):
    """Returns a list of indices of columns that are not full."""
    return [c for c in range(len(board[0])) if board[0][c] == ' ']

def input_column(valid_columns, prompt):
    """Prompts user for a column input, with validation."""
    while True:
        col_input = input(prompt).strip().upper()
        if len(col_input) != 1 or not col_input.isalpha():
            print("Invalid input: Please enter a single letter corresponding to a column.")
            continue
        col_index = ord(col_input) - ord('A')
        if col_index < 0 or col_index >= COLS:
            print("Invalid input: Column out of range.")
            continue
        if col_index not in valid_columns:
            print("Invalid move: Column is full.")
            continue
        return col_index

def make_move(board, col, checker):
    """Drops the checker into the lowest available row in the column. Returns the row index placed."""
    for row in reversed(range(len(board))):
        if board[row][col] == ' ':
            board[row][col] = checker
            return row
    return None  # Should not happen if input_column is correct

def check_win(board, player_checker):
    """Checks if the current player has 4 in a row either direction."""
    rows = len(board)
    cols = len(board[0])

    for r in range(rows):
        for c in range(cols):
            if board[r][c] != player_checker:
                continue
            # Horizontally
            if c + 3 < cols and all(board[r][c + i] == player_checker for i in range(4)):
                return True
            # Vertically
            if r + 3 < rows and all(board[r + i][c] == player_checker for i in range(4)):
                return True
            # Diagonal Down-Right
            if r + 3 < rows and c + 3 < cols and all(board[r + i][c + i] == player_checker for i in range(4)):
                return True
            # Diagonal Down-Left
            if r + 3 < rows and c - 3 >= 0 and all(board[r + i][c - i] == player_checker for i in range(4)):
                return True
    return False

def check_draw(board):
    """Returns True if all cells are filled."""
    return all(cell != ' ' for row in board for cell in row)

def main():
    # Validate board dimension constraints
    if COLS > MAX_COLS or NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
        print("Board size or number of players not allowed!")
        return
    
    board = create_board(ROWS, COLS)
    players = CHECKERS[:NUM_PLAYERS]
    player_names = ['Player {}'.format(c) for c in players]
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)
    clear_screen()
    print_board(board)
    print(f"{player_names[current_player_idx]} ({players[current_player_idx]}) starts!")

    while True:
        current_checker = players[current_player_idx]
        valid_columns = get_valid_columns(board)
        if not valid_columns:
            clear_screen()
            print_board(board)
            print("Game ends in a draw!")
            return

        prompt = f"{player_names[current_player_idx]} ({current_checker}), please enter a column: "
        col = None
        # Input and move
        while True:
            col = input_column(valid_columns, prompt)
            row = make_move(board, col, current_checker)
            break

        clear_screen()
        print_board(board)

        # Check for win
        if check_win(board, current_checker):
            print(f"{player_names[current_player_idx]} ({current_checker}) won!")
            return

        # Check for draw
        if check_draw(board):
            print("Game ends in a draw!")
            return

        # Next player
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
