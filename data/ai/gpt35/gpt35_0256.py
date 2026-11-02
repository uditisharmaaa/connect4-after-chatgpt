import os
import random

# Constants
ROWS = 6
COLS = 7
MIN_PLAYERS = 2
MAX_PLAYERS = 5
CHECKERS = ["X", "O", "V", "H", "M"]
WINNING_COUNT = 4

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    # Print column headers
    cols = len(board[0])
    header = "  " + "   ".join(chr(ord('A') + i) for i in range(cols))
    print(header)
    # Print the board rows with separators
    row_sep = "+" + "---+" * cols
    for r in range(len(board)):
        print(row_sep)
        line = "|"
        for c in range(cols):
            line += f" {board[r][c]} |"
        print(line)
    print(row_sep)

def valid_column_choice(choice, cols):
    if len(choice) != 1:
        return False
    uc = choice.upper()
    if 'A' <= uc < chr(ord('A') + cols):
        return True
    return False

def column_index_from_choice(choice):
    return ord(choice.upper()) - ord('A')

def is_column_full(board, col):
    return board[0][col] != " "

def place_checker(board, col, checker):
    # Place checker in the lowest empty row in the column
    for row in range(len(board)-1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row, col
    return None  # Column full

def check_win(board, row, col, checker):
    rows = len(board)
    cols = len(board[0])

    def count_direction(r_step, c_step):
        count = 1  # Start with the last placed checker
        # Check forward direction
        r, c = row + r_step, col + c_step
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r += r_step
            c += c_step
        # Check backward direction
        r, c = row - r_step, col - c_step
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r -= r_step
            c -= c_step
        return count

    # Horizontal (r_step=0, c_step=1)
    if count_direction(0, 1) >= WINNING_COUNT:
        return True
    # Vertical (r_step=1, c_step=0)
    if count_direction(1, 0) >= WINNING_COUNT:
        return True
    # Diagonal \ (r_step=1, c_step=1)
    if count_direction(1, 1) >= WINNING_COUNT:
        return True
    # Diagonal / (r_step=1, c_step=-1)
    if count_direction(1, -1) >= WINNING_COUNT:
        return True

    return False

def board_full(board):
    # If top row is fully occupied, board is full
    return all(cell != " " for cell in board[0])

def main():
    rows = ROWS
    cols = COLS
    num_players = 2
    players = CHECKERS[:num_players]

    board = create_board(rows, cols)
    current_player_idx = random.randint(0, num_players - 1)

    while True:
        clear_screen()
        print_board(board)
        current_checker = players[current_player_idx]
        print(f"Player {current_checker}, please enter a column:")

        # Input loop for valid input or losing turn if full column
        while True:
            choice = input().strip()
            if not valid_column_choice(choice, cols):
                print("Invalid input. Please enter a valid column letter:")
                continue
            col = column_index_from_choice(choice)
            if is_column_full(board, col):
                # According to assignment if column full, turn invalid and lost
                print("Column is full! You lost your turn.")
                break
            # Place checker
            pos = place_checker(board, col, current_checker)
            if pos is None:
                # Ideally should never hit this as is_column_full checked
                print("Unexpected error: Could not place checker. Try another column:")
                continue
            else:
                # Successfully placed checker
                break

        if pos is not None:
            r, c = pos
            # Check for win
            if check_win(board, r, c, current_checker):
                clear_screen()
                print_board(board)
                print(f"Player {current_checker} won!")
                return
            # Check draw
            if board_full(board):
                clear_screen()
                print_board(board)
                print("It's a draw!")
                return

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % num_players

if __name__ == "__main__":
    main()
