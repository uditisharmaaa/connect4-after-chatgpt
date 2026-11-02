import os
import random

# Constants for board dimensions and players
ROWS = 6            # Number of rows (height)
COLUMNS = 7         # Number of columns (width)
MIN_PLAYERS = 2     # Minimum players allowed
MAX_PLAYERS = 5     # Maximum players allowed
NUM_PLAYERS = 2     # Number of players for submission (fixed 2)
CHECKERS = ['X', 'O', 'V', 'H', 'M']  # Checkers for players in order
WIN_LENGTH = 4      # Number of consecutive checkers needed to win

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')

def create_board(rows, cols):
    """
    Creates and returns a 2D board initialized with spaces.
    Board indexed as board[row][col].
    """
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """
    Prints the board as per the format specified.
    Columns labeled A, B, C, ... without row labels.
    """
    cols = len(board[0])
    rows = len(board)
    letters = [chr(ord('A') + i) for i in range(cols)]

    # Print column headers
    print('  ' + '   '.join(letters))
    # Print top border line
    print('+' + '---+' * cols)

    # Print each row
    for row in range(rows):
        row_cells = []
        for col in range(cols):
            row_cells.append(' ' + board[row][col] + ' ')
        print('|' + '|'.join(row_cells) + '|')
        print('+' + '---+' * cols)

def valid_column_input(user_input, cols):
    """
    Checks if the user input is a valid column letter.
    Returns True if valid, else False.
    """
    if len(user_input) != 1:
        return False
    if not ('A' <= user_input <= chr(ord('A') + cols -1)):
        return False
    return True

def get_column_index(user_input):
    """
    Converts column letter to zero-based index.
    E.g., 'A' -> 0, 'B' -> 1, ...
    """
    return ord(user_input) - ord('A')

def place_checker(board, col, checker):
    """
    Places the checker in the given column at the lowest empty space.
    Returns True if placed, False if column full.
    """
    # Start from bottom row and move upwards
    for row in range(len(board)-1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = checker
            return True
    return False  # Column is full

def check_win(board, checker):
    """
    Checks if the given checker has a winning line of length WIN_LENGTH.
    Checks horizontal, vertical and diagonal wins.
    Returns True if win found, else False.
    """
    rows = len(board)
    cols = len(board[0])

    # Horizontal check
    for row in range(rows):
        for col in range(cols - WIN_LENGTH + 1):
            if all(board[row][col+i] == checker for i in range(WIN_LENGTH)):
                return True

    # Vertical check
    for col in range(cols):
        for row in range(rows - WIN_LENGTH + 1):
            if all(board[row+i][col] == checker for i in range(WIN_LENGTH)):
                return True

    # Diagonal (down-right) check
    for row in range(rows - WIN_LENGTH + 1):
        for col in range(cols - WIN_LENGTH + 1):
            if all(board[row+i][col+i] == checker for i in range(WIN_LENGTH)):
                return True

    # Diagonal (down-left) check
    for row in range(rows - WIN_LENGTH + 1):
        for col in range(WIN_LENGTH - 1, cols):
            if all(board[row+i][col-i] == checker for i in range(WIN_LENGTH)):
                return True

    return False

def check_draw(board):
    """
    Checks if the board is full (no empty spaces).
    Returns True if draw, else False.
    """
    for row in board:
        if ' ' in row:
            return False
    return True

def main():
    # Set up the game
    rows = ROWS
    cols = COLUMNS
    num_players = NUM_PLAYERS
    checkers = CHECKERS[:num_players]

    board = create_board(rows, cols)
    # Randomly select first player index
    current_player_idx = random.randint(0, num_players - 1)

    while True:
        clear_screen()
        print_board(board)
        current_checker = checkers[current_player_idx]
        prompt = f"Player {current_checker}, please enter a column: "

        # Collect valid input or lose turn if full column
        while True:
            user_input = input(prompt).strip().upper()
            if not valid_column_input(user_input, cols):
                # Invalid input (length, char)
                print(f"Invalid input. Please enter a letter between A and {chr(ord('A') + cols - 1)}.")
                continue
            col = get_column_index(user_input)
            # Check if column full
            if board[0][col] != ' ':  # Top cell is occupied means full column
                # Player loses turn on full column
                print(f"Column {user_input} is full. You lose your turn.")
                break
            else:
                # Place checker and break input loop
                placed = place_checker(board, col, current_checker)
                # placed should always be True here, but sanity check
                if placed:
                    break
                else:
                    # Should not happen, but fail-safe
                    print(f"Column {user_input} is full. You lose your turn.")
                    break

        # After turn: check for win or draw
        if check_win(board, current_checker):
            clear_screen()
            print_board(board)
            print(f"Player {current_checker} won!")
            break

        if check_draw(board):
            clear_screen()
            print_board(board)
            print("The game is a draw!")
            break

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % num_players

if __name__ == "__main__":
    main()
