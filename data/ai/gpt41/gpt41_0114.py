import os
import random
import sys
import string

# ================ CONSTANT CONFIGURATIONS ================
ROWS = 6               # Number of rows in the board
COLS = 7               # Number of columns in the board (max 26)
NUM_PLAYERS = 2        # Number of players (2 to 5)
CHECKERS = ['X', 'O', 'V', 'H', 'M']  # Player checker symbols

# ================ FUNCTION DEFINITIONS =================

def clear_screen():
    # Clears the terminal screen
    os.system('clear' if os.name != 'nt' else 'cls')


def create_board(rows, cols):
    # Creates and returns a 2D list representing the board filled with spaces
    return [[' ' for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    # Prints the board in a formatted way as described in the requirements
    
    cols = len(board[0])
    # Print column headers (A, B, C, ...)
    col_labels = "  " + "   ".join(string.ascii_uppercase[:cols])
    print(col_labels)
    print("+" + "---+" * cols)
    
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * cols)


def get_valid_column(board, player_checker):
    cols = len(board[0])
    valid_columns = [string.ascii_uppercase[i] for i in range(cols)]
    while True:
        user_input = input(f'Player {player_checker}, please enter a column: ').strip().upper()
        if len(user_input) != 1 or user_input not in valid_columns:
            print(f"Invalid input! Please enter a letter between A and {valid_columns[-1]}.")
            continue
        col_idx = valid_columns.index(user_input)
        # Check if the column is full
        if board[0][col_idx] != ' ':
            print(f"Column {user_input} is full! You lose your turn.")
            return None
        return col_idx


def drop_checker(board, col, checker):
    # Drop the checker into the specified column and return the row index where it landed
    for row in reversed(range(len(board))):
        if board[row][col] == ' ':
            board[row][col] = checker
            return row
    # If this point is reached, the column is full (should not happen if validated)
    return None


def check_line_win(line, checker):
    # Helper to check if 'checker' appears 4 times in a row in the list 'line'
    count = 0
    for x in line:
        if x == checker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
    return False


def check_win(board, checker):
    rows = len(board)
    cols = len(board[0])

    # Horizontal check
    for r in range(rows):
        if check_line_win(board[r], checker):
            return True

    # Vertical check
    for c in range(cols):
        col_array = [board[r][c] for r in range(rows)]
        if check_line_win(col_array, checker):
            return True

    # Diagonal (bottom-left to top-right)
    for r in range(rows - 3):
        for c in range(cols - 3):
            diag = [board[r + i][c + i] for i in range(4)]
            if all(x == checker for x in diag):
                return True

    # Diagonal (top-left to bottom-right)
    for r in range(3, rows):
        for c in range(cols - 3):
            diag = [board[r - i][c + i] for i in range(4)]
            if all(x == checker for x in diag):
                return True

    return False


def check_draw(board):
    # Returns True if board is full (draw), otherwise False
    return all(cell != ' ' for cell in board[0])


def get_players_checkers(num_players):
    return CHECKERS[:num_players]


def main():
    # Seed the random number generator for reproducibility (optional)
    random.seed()

    # Initialize board and players
    board = create_board(ROWS, COLS)
    player_symbols = get_players_checkers(NUM_PLAYERS)

    # Randomly select first player
    current = random.randint(0, NUM_PLAYERS - 1)

    # Print initial board
    clear_screen()
    print_board(board)

    while True:
        player_checker = player_symbols[current]
        col = get_valid_column(board, player_checker)

        if col is None:
            # The player loses the turn due to full column
            current = (current + 1) % NUM_PLAYERS
            clear_screen()
            print_board(board)
            continue

        # Place checker
        row = drop_checker(board, col, player_checker)

        clear_screen()
        print_board(board)

        # Check for win
        if check_win(board, player_checker):
            print(f"Player {player_checker} won!")
            return

        # Check for draw
        if check_draw(board):
            print("The game is a draw!")
            return

        # Go to next player
        current = (current + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
