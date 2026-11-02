import os
import random
import string

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]  # Supports up to 5 players
WIN_LENGTH = 4

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    # Print column labels
    col_labels = [string.ascii_uppercase[i] for i in range(len(board[0]))]
    print("  " + "   ".join(col_labels))
    
    # Print board rows with separators
    horiz_line = "+" + "---+" * len(board[0])
    for row in board:
        print(horiz_line)
        print("| " + " | ".join(row) + " |")
    print(horiz_line)

def get_valid_column_input(board, player_checker):
    cols = len(board[0])
    col_labels = [string.ascii_uppercase[i] for i in range(cols)]
    while True:
        user_input = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        
        if len(user_input) != 1:
            # Not a single character
            continue
        if user_input not in col_labels:
            # Not a valid column letter
            continue
        
        col_index = col_labels.index(user_input)
        # Check if the column is full
        if board[0][col_index] != " ":
            # Column full, player loses turn
            return None
        return col_index

def place_checker(board, col_index, checker):
    """Place the checker in the lowest available row of the column.
       Returns True if placed successfully, False if column full."""
    for row in reversed(range(len(board))):
        if board[row][col_index] == " ":
            board[row][col_index] = checker
            return True
    return False  # Column full

def check_win(board, checker):
    rows = len(board)
    cols = len(board[0])

    # Horizontal check
    for r in range(rows):
        count = 0
        for c in range(cols):
            if board[r][c] == checker:
                count += 1
                if count == WIN_LENGTH:
                    return True
            else:
                count = 0

    # Vertical check
    for c in range(cols):
        count = 0
        for r in range(rows):
            if board[r][c] == checker:
                count += 1
                if count == WIN_LENGTH:
                    return True
            else:
                count = 0

    # Diagonal (bottom left to top right)
    for r in range(rows - WIN_LENGTH + 1):
        for c in range(cols - WIN_LENGTH + 1):
            if all(board[r + i][c + i] == checker for i in range(WIN_LENGTH)):
                return True

    # Diagonal (top left to bottom right)
    for r in range(WIN_LENGTH - 1, rows):
        for c in range(cols - WIN_LENGTH + 1):
            if all(board[r - i][c + i] == checker for i in range(WIN_LENGTH)):
                return True

    return False

def check_draw(board):
    # Draw if top row is fully occupied (no spaces)
    return all(cell != " " for cell in board[0])

def main():
    board = create_board(ROWS, COLS)
    players = CHECKERS[:NUM_PLAYERS]

    current_player_index = random.randrange(NUM_PLAYERS)
    print_board(board)

    while True:
        current_checker = players[current_player_index]

        col = get_valid_column_input(board, current_checker)
        # If col is None, column was full -> player loses turn
        if col is None:
            # Player loses turn, just advance
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            print_board(board)
            continue

        # Place checker
        placed = place_checker(board, col, current_checker)
        if not placed:
            # Technically should not happen because we check full before
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            print_board(board)
            continue
        
        print_board(board)

        # Check win
        if check_win(board, current_checker):
            print(f"Player {current_checker} won!")
            break
        
        # Check draw
        if check_draw(board):
            print("Game ends in a draw!")
            break

        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
