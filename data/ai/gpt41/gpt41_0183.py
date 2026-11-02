import os
import random
import string

# -------------------------------
# CONSTANTS
# -------------------------------
NUM_ROWS = 6
NUM_COLS = 7   # Max 26
NUM_PLAYERS = 2  # Set to 2 for submission. Can be 2-5.

CHECKERS = ['X', 'O', 'V', 'H', 'M']

# -------------------------------
# FUNCTIONS
# -------------------------------

def clear_screen():
    """
    Clears the terminal screen.
    """
    os.system('clear')  # For Linux/Unix compatibility

def create_board(rows, cols):
    """
    Creates and returns a 2D list representing the board, filled with spaces.
    """
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """
    Prints the Connect 4 board in the specified format with column labels.
    """
    cols = len(board[0])
    # Print header row (A B C ...)
    header = '  ' + '   '.join(string.ascii_uppercase[:cols])
    print(header)
    # Print top border
    print('+' + '---+' * cols)
    # Print each row
    for row in board:
        row_str = '|' + '|'.join(f' {cell} ' for cell in row) + '|'
        print(row_str)
        print('+' + '---+' * cols)

def get_valid_column_input(board):
    """
    Prompts for a column letter, checks validity,
    and returns the corresponding column index (int).
    """
    cols = len(board[0])
    valid_letters = string.ascii_uppercase[:cols]
    while True:
        col_input = input("Please enter a column: ").strip().upper()
        if len(col_input) != 1 or col_input not in valid_letters:
            print(f"Invalid input. Enter a letter between A and {valid_letters[cols-1]}.")
            continue
        col = ord(col_input) - ord('A')
        if board[0][col] != ' ':
            print("Column is full. You lose your turn this time.")
            return None    # Lose turn if column is full
        return col

def place_checker(board, col, checker):
    """
    Drops the player's checker into the lowest available spot in the given column.
    Returns the row index where the checker lands.
    """
    for row in reversed(range(len(board))):
        if board[row][col] == ' ':
            board[row][col] = checker
            return row
    # Should not reach here as column fullness is checked outside
    return None

def check_win(board, row, col, checker):
    """
    Checks if dropping a checker at (row, col) causes a win (4 in a row!) for the player.
    Returns True if win, else False.
    """
    directions = [
        (0, 1),   # Horizontal right
        (1, 0),   # Vertical down
        (1, 1),   # Diagonal down-right
        (1, -1)   # Diagonal down-left
    ]
    rows = len(board)
    cols = len(board[0])
    for dr, dc in directions:
        count = 1
        # Check one direction
        r, c = row + dr, col + dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # Check the opposite direction
        r, c = row - dr, col - dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        if count >= 4:
            return True
    return False

def is_board_full(board):
    """
    Returns True if the board is full, else False.
    """
    return all(cell != ' ' for cell in board[0])

def main():
    # Set up
    board = create_board(NUM_ROWS, NUM_COLS)
    player_checkers = CHECKERS[:NUM_PLAYERS]
    player_names = [f"Player {c}" for c in player_checkers]
    # Randomly choose starting player
    current_player = random.randint(0, NUM_PLAYERS - 1)

    # Show initial board
    clear_screen()
    print_board(board)

    while True:
        checker = player_checkers[current_player]
        player_str = player_names[current_player]
        print(f"{player_str} ({checker}), please enter a column:")
        col = get_valid_column_input(board)

        # If column is full, lose turn (as per assignment specification)
        if col is None:
            current_player = (current_player + 1) % NUM_PLAYERS
            clear_screen()
            print_board(board)
            continue

        row = place_checker(board, col, checker)

        clear_screen()
        print_board(board)

        # Check for win
        if check_win(board, row, col, checker):
            print(f"{player_names[current_player]} won!")
            break

        # Check for draw
        if is_board_full(board):
            print("It's a draw!")
            break

        # Next player's turn
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == '__main__':
    main()
