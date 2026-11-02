import os
import random

# Constants
ROWS = 6             # Number of rows on the board
COLUMNS = 7          # Number of columns on the board (max 26)
WIN_LENGTH = 4       # Number of consecutive checkers needed to win
PLAYERS = 2          # Number of players (between 2 and 5)
CHECKERS = ['X', 'O', 'V', 'H', 'M']  # Checkers for players in order

def clear_screen():
    """Clear the terminal screen."""
    os.system('clear')

def create_board(rows, columns):
    """Create a board initialized with spaces."""
    return [[' ' for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    """Print the current board state with labels."""
    clear_screen()

    # Print column labels (A, B, C, ...)
    col_labels = [chr(ord('A') + i) for i in range(len(board[0]))]
    print('  ' + '   '.join(col_labels))

    # Print each row with separators
    for row in range(len(board)):
        print('+' + '---+' * len(board[0]))
        # Print cells with pipe separators
        print('|' + '|'.join(f' {board[row][col]} ' for col in range(len(board[0]))) + '|')
    print('+' + '---+' * len(board[0]))

def is_valid_column(input_str, columns):
    """Check if user input is a valid column letter."""
    if len(input_str) != 1:
        return False
    letter = input_str.upper()
    return 'A' <= letter < chr(ord('A') + columns)

def column_to_index(col_letter):
    """Convert column letter to index."""
    return ord(col_letter.upper()) - ord('A')

def get_next_open_row(board, col):
    """Return the lowest empty row index in the column or None if full."""
    for row in reversed(range(len(board))):
        if board[row][col] == ' ':
            return row
    return None

def place_checker(board, row, col, checker):
    """Place the player's checker at given row and column."""
    board[row][col] = checker

def check_win(board, checker):
    """Check the board for a win condition for the checker."""
    rows = len(board)
    columns = len(board[0])

    # Horizontal check
    for row in range(rows):
        for col in range(columns - WIN_LENGTH + 1):
            if all(board[row][col + offset] == checker for offset in range(WIN_LENGTH)):
                return True

    # Vertical check
    for col in range(columns):
        for row in range(rows - WIN_LENGTH + 1):
            if all(board[row + offset][col] == checker for offset in range(WIN_LENGTH)):
                return True

    # Diagonal (down-right) check
    for row in range(rows - WIN_LENGTH + 1):
        for col in range(columns - WIN_LENGTH + 1):
            if all(board[row + offset][col + offset] == checker for offset in range(WIN_LENGTH)):
                return True

    # Diagonal (down-left) check
    for row in range(rows - WIN_LENGTH + 1):
        for col in range(WIN_LENGTH - 1, columns):
            if all(board[row + offset][col - offset] == checker for offset in range(WIN_LENGTH)):
                return True

    return False

def board_full(board):
    """Check if the board is full (no spaces left in top row)."""
    return all(cell != ' ' for cell in board[0])

def main():
    # Initialize game board
    board = create_board(ROWS, COLUMNS)

    # Restricted checkers list for active players
    active_checkers = CHECKERS[:PLAYERS]

    # Randomly select starting player index
    current_player_index = random.randint(0, PLAYERS - 1)

    # Print initial board
    print_board(board)

    # Game loop
    while True:
        current_checker = active_checkers[current_player_index]
        prompt = f"Player {current_checker}, please enter a column: "
        
        # Input validation loop
        while True:
            user_input = input(prompt).strip().upper()
            if not is_valid_column(user_input, COLUMNS):
                print(f"Invalid input! Please enter a column between A and {chr(ord('A') + COLUMNS - 1)}.")
                continue

            col = column_to_index(user_input)
            open_row = get_next_open_row(board, col)
            if open_row is None:
                # Column full, player loses turn according to assignment
                print(f"Column {user_input} is full. You lose your turn.")
                break
            else:
                # Valid move: place checker and break validation loop
                place_checker(board, open_row, col, current_checker)
                break

        print_board(board)

        # If player placed a checker (not lost turn)
        if open_row is not None:
            # Check for win
            if check_win(board, current_checker):
                print(f"Player {current_checker} won!")
                break

            # Check for draw
            if board_full(board):
                print("The game is a draw!")
                break

        # Next player's turn
        current_player_index = (current_player_index + 1) % PLAYERS

if __name__ == "__main__":
    main()
