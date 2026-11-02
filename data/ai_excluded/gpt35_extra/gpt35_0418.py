import os
import random

# Constants for the game settings
ROWS = 6                # Number of rows of the board
COLS = 7                # Number of columns of the board (max 26)
PLAYERS_COUNT = 2       # Number of players (2 to 5)
CHECKERS = ['X', 'O', 'V', 'H', 'M']  # Checkers for players

def clear_screen():
    """Clear the terminal screen for Linux/Unix."""
    os.system('clear')

def create_board(rows, cols):
    """Create and return a 2D board initialized with spaces."""
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """
    Print the current state of the board.
    Columns labeled A, B, C, ...
    """
    cols = len(board[0])
    rows = len(board)
    # Print column headers
    header = '  ' + '   '.join(chr(ord('A') + i) for i in range(cols))
    print(header)
    # Print board with horizontal separators
    separator = '+' + '---+' * cols
    for r in range(rows):
        print(separator)
        # Print each cell with vertical bars
        row_str = '| ' + ' | '.join(board[r][c] for c in range(cols)) + ' |'
        print(row_str)
    print(separator)

def is_valid_column(input_str, cols):
    """
    Check if input is a valid column letter within board range.
    Must be single uppercase letter from 'A' up to last column letter.
    """
    if len(input_str) != 1:
        return False
    c = input_str[0]
    if not ('A' <= c <= chr(ord('A') + cols - 1)):
        return False
    return True

def get_column_index(col_letter):
    """Convert column letter (A-G) to zero-based index."""
    return ord(col_letter) - ord('A')

def place_checker(board, col_idx, checker):
    """
    Place the checker in the lowest available row of the column.
    Returns True if placed successfully, False if column is full.
    """
    rows = len(board)
    # Start from bottom row and go upwards
    for r in range(rows - 1, -1, -1):
        if board[r][col_idx] == ' ':
            board[r][col_idx] = checker
            return True
    return False  # Column full

def check_winner(board, checker):
    """
    Check all directions for 4 consecutive checkers for given player.
    Returns True if player has won, False otherwise.
    """
    rows = len(board)
    cols = len(board[0])
    needed = 4  # Number of consecutive checkers to win

    # Horizontal check
    for r in range(rows):
        count = 0
        for c in range(cols):
            if board[r][c] == checker:
                count += 1
                if count == needed:
                    return True
            else:
                count = 0

    # Vertical check
    for c in range(cols):
        count = 0
        for r in range(rows):
            if board[r][c] == checker:
                count += 1
                if count == needed:
                    return True
            else:
                count = 0

    # Diagonal check (top-left to bottom-right)
    for r in range(rows - needed + 1):
        for c in range(cols - needed + 1):
            if all(board[r + i][c + i] == checker for i in range(needed)):
                return True

    # Diagonal check (bottom-left to top-right)
    for r in range(needed - 1, rows):
        for c in range(cols - needed + 1):
            if all(board[r - i][c + i] == checker for i in range(needed)):
                return True

    return False

def board_full(board):
    """Check if the board is completely filled (no empty spaces)."""
    return all(cell != ' ' for row in board for cell in row)

def main():
    # Initialize game board
    board = create_board(ROWS, COLS)

    # Players' checkers (based on requested number of players)
    players_checkers = CHECKERS[:PLAYERS_COUNT]

    # Choose random starting player index
    current_player_idx = random.randint(0, PLAYERS_COUNT - 1)

    while True:
        clear_screen()
        print_board(board)

        current_checker = players_checkers[current_player_idx]
        prompt = f"Player {current_checker}, please enter a column: "

        # Input validation loop
        while True:
            user_input = input(prompt).strip().upper()
            if not is_valid_column(user_input, COLS):
                print(f"Invalid input! Please enter a letter between A and {chr(ord('A') + COLS - 1)}.")
                continue
            col_idx = get_column_index(user_input)
            # Check if column is full to handle losing turn if full
            if board[0][col_idx] != ' ':
                # Column full - turn lost
                print(f"Column {user_input} is full! You lose your turn.")
                input("Press Enter to continue...")
                break
            # Place the checker
            placed = place_checker(board, col_idx, current_checker)
            if placed:
                break
            else:
                # Redundant since we check column full above, but kept for safety
                print(f"Column {user_input} is full! You lose your turn.")
                input("Press Enter to continue...")
                break

        # If placed checker, check for winning condition
        if board[0][col_idx] == current_checker:
            if check_winner(board, current_checker):
                clear_screen()
                print_board(board)
                print(f"Player {current_checker} won!")
                break

        # Check for draw
        if board_full(board):
            clear_screen()
            print_board(board)
            print("The game is a draw!")
            break

        # Next player's turn (only if current player placed a checker)
        # If turn lost due to full column (no placement), skip increment
        if board[0][col_idx] == current_checker:
            current_player_idx = (current_player_idx + 1) % PLAYERS_COUNT
        else:
            # Turn lost, move to next player anyway
            current_player_idx = (current_player_idx + 1) % PLAYERS_COUNT

if __name__ == '__main__':
    main()
