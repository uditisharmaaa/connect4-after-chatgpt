import os
import random

# Constants (for testing, these are fixed as per submission requirement)
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]  # Only up to NUM_PLAYERS will be used

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    # Create a rows x cols board initialized with spaces
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()

    # Print column headers A, B, C ...
    header = "  " + "   ".join(chr(ord('A') + i) for i in range(len(board[0])))
    print(header)

    # Print board with the format shown in the assignment
    row_separator = "+" + "---+" * len(board[0])
    for row in board:
        print(row_separator)
        print("| " + " | ".join(row) + " |")
    print(row_separator)

def get_player_input(player_checker, board):
    cols = len(board[0])
    valid_letters = [chr(ord('A') + i) for i in range(cols)]
    while True:
        choice = input(f"Player {player_checker}, please enter a column: ")
        # Validate length 1, uppercase letter in range
        if len(choice) != 1 or choice not in valid_letters:
            continue
        col = ord(choice) - ord('A')

        # Check if column is full - if so, player loses turn
        if board[0][col] != " ":
            # Column full, lose turn silently (return None)
            return None
        else:
            return col

def place_checker(board, col, checker):
    # Start from bottom row to top row to find first empty cell
    for row in range(len(board)-1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row, col
    # Should not happen if checked before call
    return None

def check_win(board, row, col, checker):
    rows = len(board)
    cols = len(board[0])

    # Directions represented as (delta_row, delta_col)
    directions = [
        (0, 1),   # horizontal right
        (1, 0),   # vertical down
        (1, 1),   # diagonal down-right
        (1, -1)   # diagonal down-left
    ]

    for dr, dc in directions:
        count = 1  # count includes the newly placed checker

        # Check in positive direction
        r, c = row + dr, col + dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r += dr
            c += dc

        # Check in negative direction
        r, c = row - dr, col - dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc

        if count >= WIN_LENGTH:
            return True
    return False

def board_full(board):
    # If top row contains no empty spaces, board is full
    return all(cell != " " for cell in board[0])

def main():
    board = create_board(ROWS, COLS)
    players = PLAYER_CHECKERS[:NUM_PLAYERS]

    # Randomly select starting player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)

    print_board(board)

    while True:
        checker = players[current_player_index]
        col = get_player_input(checker, board)

        if col is None:
            # Invalid turn: full column entered, player loses turn
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            continue

        rowcol = place_checker(board, col, checker)
        print_board(board)
        row, col_placed = rowcol

        if check_win(board, row, col_placed, checker):
            print(f"Player {checker} won!")
            break

        if board_full(board):
            print("The game is a draw!")
            break

        # Next player's turn
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
