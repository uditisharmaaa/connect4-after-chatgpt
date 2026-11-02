import os
import random

# Constants (change here for different board sizes or number of players)
ROWS = 6                # Number of rows
COLUMNS = 7             # Number of columns (max 26)
PLAYERS = 2             # Number of players (2 to 5)
CHECKERS = ['X', 'O', 'V', 'H', 'M']  # Player checkers in order

# Validate PLAYERS to fit within CHECKERS list
PLAYERS = max(2, min(PLAYERS, 5))

def clear_screen():
    """Clear the terminal screen."""
    os.system('clear')

def create_board():
    """Create a ROWS x COLUMNS board filled with spaces."""
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    """Print the board with column headers as letters starting from A."""
    clear_screen()
    # Print column labels (A, B, C, ...)
    column_labels = [chr(ord('A') + i) for i in range(COLUMNS)]
    print('  ' + '   '.join(column_labels))
    
    # Print each row with cell borders
    horizontal_line = '+' + ('---+' * COLUMNS)
    for row in range(ROWS):
        print(horizontal_line)
        row_cells = []
        for col in range(COLUMNS):
            row_cells.append(f' {board[row][col]} ')
        print('|' + '|'.join(row_cells) + '|')
    print(horizontal_line)

def input_column(player_checker):
    """Prompt player to input a column letter, validating input."""
    while True:
        col_input = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        # Must be a single letter A to appropriate letter
        if len(col_input) != 1:
            print("Invalid input: Enter exactly one letter corresponding to a column.")
            continue
        col_index = ord(col_input) - ord('A')
        if col_index < 0 or col_index >= COLUMNS:
            print(f"Invalid input: Please enter a letter between A and {chr(ord('A') + COLUMNS -1)}.")
            continue
        return col_index

def place_checker(board, col_index, player_checker):
    """
    Place the checker in the correct row for the chosen column.
    Returns tuple (success(bool), row_index(int)) - row_index is None if unsuccessful.
    If column is full, return (False, None)
    """
    for row_index in reversed(range(ROWS)):
        if board[row_index][col_index] == ' ':
            board[row_index][col_index] = player_checker
            return True, row_index
    # Column full, player loses the turn
    return False, None

def check_winner(board, player_checker, row, col):
    """
    Check win condition after last move at (row, col) for player_checker.
    Returns True if player has 4 in a row horizontally, vertically, or diagonally.
    """

    def count_direction(delta_row, delta_col):
        """Count consecutive checkers of player_checker starting at (row,col) in given direction."""
        r, c = row + delta_row, col + delta_col
        count = 0
        while 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == player_checker:
            count += 1
            r += delta_row
            c += delta_col
        return count

    # Directions to check: horizontal, vertical and two diagonals
    directions = [
        ((0, 1), (0, -1)),    # horizontal right & left
        ((1, 0), (-1, 0)),    # vertical down & up
        ((1, 1), (-1, -1)),   # diagonal down-right & up-left
        ((1, -1), (-1, 1))    # diagonal down-left & up-right
    ]

    for dir_pair in directions:
        total_count = 1  # Count current checker
        for delta in dir_pair:
            total_count += count_direction(*delta)
        if total_count >= 4:
            return True
    return False

def board_full(board):
    """Return True if the board is full (no empty spaces), else False."""
    for row in board:
        if ' ' in row:
            return False
    return True

def main():
    board = create_board()
    # Select random first player index
    current_player_idx = random.randint(0, PLAYERS - 1)

    print_board(board)

    while True:
        player_checker = CHECKERS[current_player_idx]
        # Input and validation loop for placing checker
        col_index = input_column(player_checker)
        success, row_index = place_checker(board, col_index, player_checker)
        if not success:
            # Column full - player loses turn (no retry)
            print(f"Column {chr(col_index + ord('A'))} is full. Player {player_checker} loses this turn.")
        else:
            print_board(board)
            # Check if this move wins the game
            if check_winner(board, player_checker, row_index, col_index):
                print(f"Player {player_checker} won!")
                break
            # Check for draw
            if board_full(board):
                print("The game is a draw!")
                break

        # Move to next player
        current_player_idx = (current_player_idx + 1) % PLAYERS

if __name__ == "__main__":
    main()
