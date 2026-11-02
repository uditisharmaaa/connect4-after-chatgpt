import os
import random
import string

# --- Global Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2
WIN_CONDITION = 4  # Number of checkers in a row to win

PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]
BOARD_EMPTY_CELL = " "

# --- Board Initialization and Printing ---

def create_board(rows, cols):
    """
    Creates an empty Connect 4 board.
    """
    return [[BOARD_EMPTY_CELL for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """
    Prints the current state of the Connect 4 board.
    """
    os.system('clear')  # Clear the screen

    # Print column labels (A, B, C, ...)
    print("  " + "   ".join(string.ascii_uppercase[:NUM_COLS]))

    # Print board rows
    for r in range(NUM_ROWS):
        print("+---" * NUM_COLS + "+")
        row_str = "|"
        for c in range(NUM_COLS):
            row_str += f" {board[r][c]} |"
        print(row_str)
    print("+---" * NUM_COLS + "+")

# --- Game Logic ---

def get_column_input(player_name):
    """
    Prompts the current player for a column input and validates it.
    Returns the 0-indexed column number.
    """
    while True:
        col_char = input(f"Player {player_name}, please enter a column: ").upper()
        if len(col_char) == 1 and 'A' <= col_char <= string.ascii_uppercase[NUM_COLS - 1]:
            return ord(col_char) - ord('A')
        else:
            print("Invalid input. Please enter a single uppercase letter corresponding to a column.")

def place_checker(board, col, checker):
    """
    Places the checker in the lowest available space in the specified column.
    Returns True if successful, False if the column is full.
    """
    for r in range(NUM_ROWS - 1, -1, -1):
        if board[r][col] == BOARD_EMPTY_CELL:
            board[r][col] = checker
            return True
    return False

def check_win(board, checker):
    """
    Checks if the given checker has formed a winning line (horizontal, vertical, or diagonal).
    """
    # Check horizontal
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS - WIN_CONDITION + 1):
            if all(board[r][c + i] == checker for i in range(WIN_CONDITION)):
                return True

    # Check vertical
    for r in range(NUM_ROWS - WIN_CONDITION + 1):
        for c in range(NUM_COLS):
            if all(board[r + i][c] == checker for i in range(WIN_CONDITION)):
                return True

    # Check diagonal (top-left to bottom-right)
    for r in range(NUM_ROWS - WIN_CONDITION + 1):
        for c in range(NUM_COLS - WIN_CONDITION + 1):
            if all(board[r + i][c + i] == checker for i in range(WIN_CONDITION)):
                return True

    # Check diagonal (bottom-left to top-right)
    for r in range(WIN_CONDITION - 1, NUM_ROWS):
        for c in range(NUM_COLS - WIN_CONDITION + 1):
            if all(board[r - i][c + i] == checker for i in range(WIN_CONDITION)):
                return True

    return False

def check_draw(board):
    """
    Checks if the board is completely full, indicating a draw.
    """
    return all(board[r][c] != BOARD_EMPTY_CELL for r in range(NUM_ROWS) for c in range(NUM_COLS))

def main():
    board = create_board(NUM_ROWS, NUM_COLS)
    players = PLAYER_CHECKERS[:NUM_PLAYERS]
    current_player_index = random.randint(0, NUM_PLAYERS - 1)

    game_over = False
    while not game_over:
        current_player_checker = players[current_player_index]
        print_board(board)
        print(f"Player {current_player_checker}, please enter a column:")

        valid_turn = False
        while not valid_turn:
            col_index = get_column_input(current_player_checker)
            if place_checker(board, col_index, current_player_checker):
                valid_turn = True
            else:
                print(f"Column {string.ascii_uppercase[col_index]} is full. Please choose another column.")
                # The turn is not lost, player is asked for new input.

        print_board(board) # Print board after successful placement

        if check_win(board, current_player_checker):
            print(f"Player {current_player_checker} won!")
            game_over = True
        elif check_draw(board):
            print("It's a draw!")
            game_over = True
        else:
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
