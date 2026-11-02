import os
import random
import string

# Constants
ROWS = 6
COLUMNS = 7
MIN_PLAYERS = 2
MAX_PLAYERS = 5
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_LENGTH = 4

# Number of players (must be between MIN_PLAYERS and MAX_PLAYERS)
NUM_PLAYERS = 2  # For submission, fixed to 2

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    header = "  " + "   ".join(string.ascii_uppercase[:len(board[0])])
    separator = "+" + "---+" * len(board[0])
    print(header)
    print(separator)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print(separator)

def input_column(current_player, cols, board):
    valid_columns = set(string.ascii_uppercase[:cols])
    while True:
        user_input = input(f"Player {current_player}, please enter a column: ").strip().upper()
        if len(user_input) != 1:
            print(f"Invalid input. Enter a single letter from A to {string.ascii_uppercase[cols-1]}.")
            continue
        if user_input not in valid_columns:
            print(f"Invalid column. Enter a letter from A to {string.ascii_uppercase[cols-1]}.")
            continue
        col = ord(user_input) - ord('A')
        if board[0][col] != " ":
            # Top cell filled - column full
            print(f"Column {user_input} is full. You lose your turn.")
            return None
        return col

def place_checker(board, col, checker):
    # Place checker at the lowest empty row in the given column
    for r in range(len(board)-1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return r, col
    # Should never reach here if called after checking column is not full
    return None

def check_win(board, row, col, checker):
    directions = [
        (0, 1),   # horizontal right
        (1, 0),   # vertical down
        (1, 1),   # diagonal down-right
        (1, -1),  # diagonal down-left
    ]
    rows = len(board)
    cols = len(board[0])

    for dr, dc in directions:
        count = 1  # count the checker itself

        # Check in the positive direction
        r, c = row + dr, col + dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r += dr
            c += dc

        # Check in the negative direction
        r, c = row - dr, col - dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc

        if count >= WIN_LENGTH:
            return True
    return False

def board_is_full(board):
    # If top row has any empty space, board is not full
    return all(cell != " " for cell in board[0])

def main():
    board = create_board(ROWS, COLUMNS)
    players = CHECKERS[:NUM_PLAYERS]

    # Randomly select first player index
    current_index = random.randrange(NUM_PLAYERS)

    print_board(board)

    while True:
        current_player = players[current_index]
        col = input_column(current_player, COLUMNS, board)
        if col is None:
            # Column full: player loses turn, go to next player
            current_index = (current_index + 1) % NUM_PLAYERS
            print_board(board)
            continue

        placed = place_checker(board, col, current_player)
        if placed is None:
            # Defensive check, should not happen as input_column checks already
            current_index = (current_index + 1) % NUM_PLAYERS
            print_board(board)
            continue

        print_board(board)

        row_placed, col_placed = placed
        if check_win(board, row_placed, col_placed, current_player):
            print(f"Player {current_player} won!")
            break

        if board_is_full(board):
            print("Game is a draw.")
            break

        current_index = (current_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
