import os
import random
import string
import sys

# === CONSTANTS ===
NUM_ROWS = 6
NUM_COLS = 7
PLAYERS = 2  # Set to 2 for submission. Can be changed from 2 to 5.
CHECKERS = ["X", "O", "V", "H", "M"]
BOARD_EMPTY = " "

# === FUNCTIONS ===

def clear_screen():
    """
    Clears the terminal screen.
    """
    os.system('clear')

def create_board(rows, cols):
    """
    Creates a board as a 2D list (list of lists).
    """
    return [[BOARD_EMPTY for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """
    Prints the board in the required format.
    """
    # Print column labels (A, B, ...)
    col_labels = "  " + "   ".join(string.ascii_uppercase[:len(board[0])])
    print(col_labels)
    # Print the separator
    print("+" + "---+" * len(board[0]))
    # Print each row
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * len(board[0]))

def get_valid_columns(board):
    """
    Returns a list of column indices that are not full.
    """
    valid_cols = []
    for col in range(len(board[0])):
        if board[0][col] == BOARD_EMPTY:
            valid_cols.append(col)
    return valid_cols

def get_player_input(board, player_checker):
    """
    Prompts the current player for a column letter and validates input.
    Returns a valid column index or None if the column is full.
    """
    valid_col_letters = [string.ascii_uppercase[i] for i in range(len(board[0]))]
    while True:
        player_input = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        # Input must be a single uppercase letter matching a valid column
        if player_input in valid_col_letters:
            col_index = valid_col_letters.index(player_input)
            if board[0][col_index] != BOARD_EMPTY:
                print("That column is full! You lose your turn.")
                return None
            return col_index
        else:
            print("Invalid input. Please enter a valid column letter (e.g. A, B, ...).")

def place_checker(board, col, checker):
    """
    Places the checker in the lowest available position in the given column.
    Returns the (row, col) position, or None if the column is full.
    """
    for row in reversed(range(len(board))):
        if board[row][col] == BOARD_EMPTY:
            board[row][col] = checker
            return (row, col)
    return None  # This should not happen if called with a valid column.

def is_winner(board, last_row, last_col, checker):
    """
    Checks if placing 'checker' at (last_row, last_col) causes a win.
    """
    directions = [
        (0, 1),   # Horizontal
        (1, 0),   # Vertical
        (1, 1),   # Diagonal down-right
        (-1, 1)   # Diagonal up-right
    ]
    for dr, dc in directions:
        count = 1
        # Check in the positive direction
        r, c = last_row + dr, last_col + dc
        while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # Check in the negative direction
        r, c = last_row - dr, last_col - dc
        while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        if count >= 4:
            return True
    return False

def is_draw(board):
    """
    Checks if the board is full (draw).
    """
    return all(cell != BOARD_EMPTY for cell in board[0])

def main():
    # Initialize board
    board = create_board(NUM_ROWS, NUM_COLS)
    # Set up players
    player_checkers = CHECKERS[:PLAYERS]
    # Randomly select first player
    current_player = random.randint(0, PLAYERS - 1)

    # Print empty board at start
    clear_screen()
    print_board(board)
    print(f"Player {player_checkers[current_player]} goes first!\n")

    num_moves = 0
    while True:
        # Get input and validate
        col = get_player_input(board, player_checkers[current_player])
        clear_screen()
        if col is None:
            print_board(board)
            # Advance to next player even if column is full (loses turn)
            current_player = (current_player + 1) % PLAYERS
            continue
        # Place the checker
        place = place_checker(board, col, player_checkers[current_player])
        num_moves += 1
        clear_screen()
        print_board(board)
        # Check for win
        if is_winner(board, place[0], place[1], player_checkers[current_player]):
            print(f"Player {player_checkers[current_player]} won!")
            break
        # Check for draw
        if is_draw(board):
            print("The game is a draw!")
            break
        # Next player's turn
        current_player = (current_player + 1) % PLAYERS

# Run the game (only if the script is run directly)
if __name__ == '__main__':
    main()
