import os
import random
import string

# ----- CONSTANTS -----
BOARD_ROWS = 6            # Number of rows of the board
BOARD_COLS = 7            # Number of columns of the board (max 26)
NUM_PLAYERS = 2           # Number of players (between 2 and 5)
CHECKERS = ["X", "O", "V", "H", "M"]  # Up to 5 checkers for 5 players (can add more if needed)

# Use only as many checkers as players
PLAYER_CHECKERS = CHECKERS[:NUM_PLAYERS]

# ----- FUNCTIONS -----

def clear_screen():
    """ Clears the terminal screen using the appropriate system call. """
    os.system('clear')

def create_board(rows, cols):
    """ Returns a 2D list initialized with spaces. """
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """ Prints the game board in the given format. """
    clear_screen()
    cols = len(board[0])
    # Print column labels (A, B, C, ...)
    col_labels = [string.ascii_uppercase[i] for i in range(cols)]
    print("  " + "   ".join(col_labels))
    print("+" + "---+" * cols)
    # Print each row
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * cols)

def select_first_player(num_players):
    """ Randomly selects starting player index for NUM_PLAYERS. """
    return random.randint(0, num_players - 1)

def get_column_input(valid_cols):
    """
    Prompts user for column input.
    Validates that input is a single upper-case letter, and in valid_cols.
    Returns the zero-based column index or None if input is invalid.
    """
    while True:
        user_input = input("Please enter a column: ").strip().upper()
        if len(user_input) != 1 or user_input not in valid_cols:
            print("Invalid input. Choose a letter from", ", ".join(valid_cols))
            continue
        return valid_cols.index(user_input)

def is_column_full(board, col):
    """ Returns True if a column is full, else False. """
    return all(board[row][col] != " " for row in range(len(board)))

def place_checker(board, col, checker):
    """
    Places checker in the lowest empty spot of the given column.
    Returns row index if successful, else None if column is full.
    """
    for row in reversed(range(len(board))):
        if board[row][col] == " ":
            board[row][col] = checker
            return row
    return None

def check_direction(board, row, col, dx, dy, checker):
    """
    Checks if there are 4 consecutive checkers in the specified direction
    (dx, dy) starting from (row, col).
    Returns True if found, else False.
    """
    count = 0
    r, c = row, col
    rows = len(board)
    cols = len(board[0])
    while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
        count += 1
        r += dx
        c += dy
    return count

def check_for_win(board, row, col, checker):
    """
    Checks if the given move at (row, col) causes checker to win.
    Looks in all 4 directions; returns True if found.
    """
    # Directions:   vertical, horizontal, diag \, diag /
    directions = [ (1,0), (0,1), (1,1), (1,-1) ]
    for dx, dy in directions:
        count = 1 # Count self
        # Count backwards
        r, c = row-dx, col-dy
        while 0<=r<len(board) and 0<=c<len(board[0]) and board[r][c]==checker:
            count += 1
            r -= dx
            c -= dy
        # Count forwards
        r, c = row+dx, col+dy
        while 0<=r<len(board) and 0<=c<len(board[0]) and board[r][c]==checker:
            count += 1
            r += dx
            c += dy
        if count >= 4:
            return True
    return False

def is_draw(board):
    """ Returns True if there are no empty spaces left on the board. """
    return all(cell != " " for row in board for cell in row)

def print_welcome():
    """ Prints a welcome message and instructions. """
    print("Welcome to Connect 4!")
    print(f"Board size: {BOARD_ROWS}x{BOARD_COLS}, Players: {NUM_PLAYERS}")
    print("Players' checkers:", ", ".join(PLAYER_CHECKERS))
    print("Get 4 in a row (horizontally/vertically/diagonally) to win.")
    input("Press Enter to begin...")

# ----- MAIN FUNCTIONALITY -----

def main():
    # Print welcome
    print_welcome()

    board = create_board(BOARD_ROWS, BOARD_COLS)
    col_labels = [string.ascii_uppercase[i] for i in range(BOARD_COLS)]
    player_names = [f"Player {checker}" for checker in PLAYER_CHECKERS]

    # Select first player at random
    current_player = select_first_player(NUM_PLAYERS)
    checker = PLAYER_CHECKERS[current_player]

    print_board(board)
    print(f"{player_names[current_player]} ({checker}) goes first!")

    while True:
        checker = PLAYER_CHECKERS[current_player]
        player_name = player_names[current_player]
        print_board(board)
        print(f"{player_name} ({checker}), please enter a column:")

        col = get_column_input(col_labels)
        if is_column_full(board, col):
            print("Column is full! You lose your turn.")
        else:
            # Place checker
            row = place_checker(board, col, checker)
            if check_for_win(board, row, col, checker):
                print_board(board)
                print(f"{player_name} ({checker}) won!")
                break
            elif is_draw(board):
                print_board(board)
                print("Game is a draw!")
                break
        # Switch to next player
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
