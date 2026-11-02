import os
import random
import sys

# --- Global Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2
WIN_CONDITION = 4  # Number of checkers in a row to win

PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]
EMPTY_CELL = " "

# --- Board Initialization and Display ---

def create_board(rows, cols):
    """
    Creates an empty Connect 4 board.
    """
    return [[EMPTY_CELL for _ in range(cols)] for _ in range(rows)]

def get_column_labels(cols):
    """
    Generates uppercase letter labels for columns.
    """
    labels = []
    for i in range(cols):
        if i < 26:  # For A-Z
            labels.append(chr(ord('A') + i))
        else:
            # Handle beyond Z if more than 26 columns are ever used
            # This assignment specifies max 26, so this might not be strictly needed.
            # For simplicity, let's just use A-Z for now, given the constraint.
            labels.append(chr(ord('A') + i - 26) + chr(ord('A') + i // 26 - 1))
    return labels

def print_board(board, col_labels):
    """
    Prints the Connect 4 board with column labels.
    """
    os.system('clear')  # Clear screen before printing

    # Print column labels
    print(" ", end="")
    for label in col_labels:
        print(f" {label} ", end="")
    print()

    # Print top border
    print("+", end="")
    for _ in range(len(col_labels)):
        print("---+", end="")
    print()

    # Print rows
    for row in board:
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
        print("+", end="")
        for _ in range(len(col_labels)):
            print("---+", end="")
        print()

# --- Game Logic ---

def get_player_input(current_player_checker, col_labels, board):
    """
    Prompts the current player for a column input and validates it.
    Returns the 0-indexed column number.
    """
    while True:
        try:
            player_input = input(f"Player {current_player_checker}, please enter a column: ").strip().upper()

            if not player_input:
                print("Input cannot be empty. Please enter a column letter.")
                continue

            if player_input not in col_labels:
                print(f"Invalid column '{player_input}'. Please enter a letter from {col_labels[0]} to {col_labels[-1]}.")
                continue

            col_index = col_labels.index(player_input)

            if board[0][col_index] != EMPTY_CELL:  # Check if the top row of the column is occupied
                print(f"Column {player_input} is full. Please choose another column.")
                continue

            return col_index

        except ValueError:
            print("Invalid input. Please enter a single letter for the column.")
        except IndexError:
            # This should ideally be caught by `player_input not in col_labels`
            # but as a safeguard.
            print(f"Invalid column. Please enter a letter from {col_labels[0]} to {col_labels[-1]}.")


def drop_checker(board, col_index, checker):
    """
    Places the checker in the lowest available space in the specified column.
    Returns True if successful, False if the column is full (though this should be
    checked before calling this function).
    """
    for r in range(len(board) - 1, -1, -1):
        if board[r][col_index] == EMPTY_CELL:
            board[r][col_index] = checker
            return True, r, col_index  # Return success and position
    return False, -1, -1  # Column was full

def check_win(board, checker, last_row, last_col):
    """
    Checks if the last placed checker resulted in a win (4 in a row).
    Checks horizontally, vertically, and diagonally.
    """
    rows = len(board)
    cols = len(board[0])

    # Helper function to count consecutive checkers
    def count_consecutive(r, c, dr, dc):
        count = 0
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        return count

    # Check horizontal
    count = count_consecutive(last_row, last_col, 0, 1) + count_consecutive(last_row, last_col, 0, -1) - 1
    if count >= WIN_CONDITION:
        return True

    # Check vertical
    count = count_consecutive(last_row, last_col, 1, 0) + count_consecutive(last_row, last_col, -1, 0) - 1
    if count >= WIN_CONDITION:
        return True

    # Check diagonal (top-left to bottom-right)
    count = count_consecutive(last_row, last_col, 1, 1) + count_consecutive(last_row, last_col, -1, -1) - 1
    if count >= WIN_CONDITION:
        return True

    # Check diagonal (top-right to bottom-left)
    count = count_consecutive(last_row, last_col, 1, -1) + count_consecutive(last_row, last_col, -1, 1) - 1
    if count >= WIN_CONDITION:
        return True

    return False

def check_draw(board):
    """
    Checks if the board is full, resulting in a draw.
    """
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == EMPTY_CELL:
                return False  # Found an empty cell, not a draw
    return True  # No empty cells found, it's a draw

def main():
    """
    Main function to run the Connect 4 game.
    """
    if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
        print("Error: Number of players must be between 2 and 5.")
        sys.exit(1)
    if NUM_COLS > 26:
        print("Error: Number of columns exceeds the maximum of 26 (A-Z).")
        sys.exit(1)

    board = create_board(NUM_ROWS, NUM_COLS)
    col_labels = get_column_labels(NUM_COLS)
    players = PLAYER_CHECKERS[:NUM_PLAYERS]

    # Randomly select the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    current_player_checker = players[current_player_index]

    print_board(board, col_labels)
    print(f"Player {current_player_checker} goes first!")

    game_over = False
    winner_checker = None

    while not game_over:
        current_player_checker = players[current_player_index]
        
        col_index = get_player_input(current_player_checker, col_labels, board)
        
        # Drop the checker
        success, last_row, last_col = drop_checker(board, col_index, current_player_checker)

        # Print the updated board
        print_board(board, col_labels)

        if success:
            # Check for win
            if check_win(board, current_player_checker, last_row, last_col):
                winner_checker = current_player_checker
                game_over = True
            # Check for draw if no win
            elif check_draw(board):
                game_over = True
            else:
                # Next player's turn
                current_player_index = (current_player_index + 1) % NUM_PLAYERS
        # else:
        #     # This branch should ideally not be hit if get_player_input handles full columns correctly
        #     # and doesn't return an index for a full column.
        #     print("Something went wrong placing the checker. This shouldn't happen.")


    # End of game messages
    if winner_checker:
        print(f"Player {winner_checker} won!")
    else:
        print("The game is a draw!")

if __name__ == "__main__":
    main()
