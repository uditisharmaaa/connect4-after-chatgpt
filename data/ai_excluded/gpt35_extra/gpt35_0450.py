import os
import random

# Constants for board dimensions and number of players
ROWS = 6        # Number of rows on the board
COLS = 7        # Number of columns on the board (max 26)
NUM_PLAYERS = 2 # Number of players (between 2 and 5)
WIN_COUNT = 4   # Number of checkers in a row needed to win

# Checkers for each player in order
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')

def create_board(rows, cols):
    """Creates an empty board with specified rows and columns."""
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Prints the board with column labels and grid as per the assignment format."""
    clear_screen()
    # Print column labels (A, B, C, ...)
    col_labels = [chr(ord('A') + i) for i in range(len(board[0]))]
    print('  ' + '   '.join(col_labels))
    # Print the board rows with '+' separator lines
    line = '+' + ('---+' * len(board[0]))
    for row in range(len(board)):
        print(line)
        # Print each cell in the row with vertical bars
        print('|' + '|'.join(f' {board[row][col]} ' for col in range(len(board[0]))) + '|')
    print(line)

def get_valid_column_input(player, board):
    """
    Prompts the current player to enter a valid column letter.
    Validates input until a correct column is given, or column is full (loses turn).
    Returns the column index or None if column full (loss of turn).
    """
    cols = len(board[0])
    col_labels = [chr(ord('A') + i) for i in range(cols)]
    while True:
        user_input = input(f"Player {player}, please enter a column: ").strip().upper()
        if len(user_input) != 1:
            print("Invalid input. Enter a single column letter.")
            continue
        if user_input not in col_labels:
            print(f"Invalid column. Please enter a letter between A and {col_labels[-1]}.")
            continue
        col_index = ord(user_input) - ord('A')
        # Check if column is full
        if board[0][col_index] != ' ':
            # Column full, player loses turn
            print("Column is full. You lose your turn.")
            return None
        return col_index

def place_checker(board, col_index, checker):
    """
    Places the checker in the selected column at the lowest available row.
    Returns True if placed successfully.
    """
    for row in reversed(range(len(board))):
        if board[row][col_index] == ' ':
            board[row][col_index] = checker
            return True
    # Should not reach here if caller checked for full column
    return False

def check_winner(board, checker):
    """
    Checks the entire board for a winning sequence of 4 checkers for the given checker.
    Returns True if player has won, False otherwise.
    """
    rows = len(board)
    cols = len(board[0])

    # Check horizontal
    for r in range(rows):
        for c in range(cols - WIN_COUNT + 1):
            if all(board[r][c + i] == checker for i in range(WIN_COUNT)):
                return True

    # Check vertical
    for c in range(cols):
        for r in range(rows - WIN_COUNT + 1):
            if all(board[r + i][c] == checker for i in range(WIN_COUNT)):
                return True

    # Check diagonal down-right
    for r in range(rows - WIN_COUNT + 1):
        for c in range(cols - WIN_COUNT + 1):
            if all(board[r + i][c + i] == checker for i in range(WIN_COUNT)):
                return True

    # Check diagonal up-right
    for r in range(WIN_COUNT - 1, rows):
        for c in range(cols - WIN_COUNT + 1):
            if all(board[r - i][c + i] == checker for i in range(WIN_COUNT)):
                return True

    return False

def board_full(board):
    """Returns True if the board has no empty spaces, else False."""
    return all(cell != ' ' for row in board for cell in row)

def main():
    # Initialize the board
    board = create_board(ROWS, COLS)

    # Setup players checkers limited by NUM_PLAYERS
    players = CHECKERS[:NUM_PLAYERS]

    # Randomly select first player index
    current_player_idx = random.randint(0, NUM_PLAYERS -1)

    # Print initial empty board
    print_board(board)

    # Game loop
    while True:
        current_checker = players[current_player_idx]

        # Get player input for move
        col_index = get_valid_column_input(current_checker, board)
        if col_index is not None:
            # Place checker in that column
            place_checker(board, col_index, current_checker)

            # Print updated board
            print_board(board)

            # Check if current player won
            if check_winner(board, current_checker):
                print(f"Player {current_checker} won!")
                break

            # Check if draw
            if board_full(board):
                print("The game is a draw!")
                break
        else:
            # Column full, lose turn, just print board again
            print_board(board)

        # Switch to next player
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
