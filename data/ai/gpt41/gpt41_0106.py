import os
import random
import string

# ----------------------------
# CONSTANTS (Change as needed)
# ----------------------------
ROWS = 6                 # number of rows
COLUMNS = 7              # number of columns (max 26)
NUM_PLAYERS = 2          # between 2 and 5
CHECKERS = ["X", "O", "V", "H", "M"]  # Player marker symbols
WIN_LENGTH = 4           # number of checkers in a row to win

# Column labels (A-Z)
COLUMN_LABELS = [chr(ord('A') + i) for i in range(COLUMNS)]

# ----------------------------
# FUNCTIONS
# ----------------------------

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')

def create_board(rows, columns):
    """Initializes the game board with empty spaces."""
    return [[' ' for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    """Prints the current state of the board."""
    clear_screen()
    # Print column headers
    header = '  ' + '   '.join(COLUMN_LABELS[:len(board[0])])
    print(header)
    print('+' + '---+' * len(board[0]))
    for row in board:
        row_str = '| ' + ' | '.join(row) + ' |'
        print(row_str)
        print('+' + '---+' * len(board[0]))

def get_valid_columns(board):
    """Returns a list of column indices that are not full."""
    valid_columns = []
    for col in range(len(board[0])):
        if board[0][col] == ' ':
            valid_columns.append(col)
    return valid_columns

def input_column(player_checker, board):
    """
    Prompts the player for a valid column input.
    Repeats until a valid column is entered or returns None if column is full (loses turn).
    """
    valid_columns = get_valid_columns(board)
    while True:
        user_input = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        if len(user_input) != 1 or user_input not in COLUMN_LABELS[:len(board[0])]:
            print(f"Invalid input. Please enter a valid column letter ({COLUMN_LABELS[0]}-{COLUMN_LABELS[len(board[0])-1]}).")
            continue
        column = COLUMN_LABELS.index(user_input)
        if board[0][column] != ' ':
            print("That column is full. You lose your turn.")
            return None
        return column

def drop_checker(board, column, checker):
    """Drops a checker into the specified column (returns row placed), or None if column full."""
    for row in reversed(range(len(board))):
        if board[row][column] == ' ':
            board[row][column] = checker
            return row
    return None  # Column full

def is_within_board(row, col, board):
    """Returns True if (row, col) is within the board limits."""
    return 0 <= row < len(board) and 0 <= col < len(board[0])

def check_win(board, row, col, checker):
    """
    Checks for a win from the position (row, col) for the given checker,
    in all 4 directions: horizontal, vertical, 2 diagonals.
    """
    directions = [
        (0, 1),   # Horizontal
        (1, 0),   # Vertical
        (1, 1),   # Diagonal (down-right)
        (1, -1),  # Diagonal (down-left)
    ]
    for dr, dc in directions:
        count = 1  # Count the current checker
        for dir in [1, -1]:  # Check both positive and negative directions
            r, c = row, col
            while True:
                r += dr * dir
                c += dc * dir
                if is_within_board(r, c, board) and board[r][c] == checker:
                    count += 1
                else:
                    break
        if count >= WIN_LENGTH:
            return True
    return False

def check_draw(board):
    """Returns True if the board is full and no more moves can be made."""
    for cell in board[0]:
        if cell == ' ':
            return False
    return True

# ----------------------------
# MAIN GAME LOOP
# ----------------------------

def main():
    # Choose checkers based on number of players
    players = CHECKERS[:NUM_PLAYERS]

    # Create the game board
    board = create_board(ROWS, COLUMNS)

    # Select a random starting player
    current_player = random.randint(0, NUM_PLAYERS - 1)

    # Print initial board
    print_board(board)

    while True:
        player_checker = players[current_player]
        col = input_column(player_checker, board)
        if col is not None:
            row_placed = drop_checker(board, col, player_checker)
            print_board(board)
            if check_win(board, row_placed, col, player_checker):
                print(f"Player {player_checker} won!")
                break
            elif check_draw(board):
                print("It's a draw!")
                break
        else:
            # Lost turn due to attempting in full column
            print_board(board)
        # Move to next player
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
