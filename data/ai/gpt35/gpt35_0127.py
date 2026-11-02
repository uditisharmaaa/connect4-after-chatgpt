import os
import random
import string

# Constants (board size and players)
ROWS = 6
COLS = 7
MIN_PLAYERS = 2
MAX_PLAYERS = 5
NUM_PLAYERS = 2  # As required by submission instructions

CHECKERS = ["X", "O", "V", "H", "M"][0:NUM_PLAYERS]

EMPTY_CELL = " "

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[EMPTY_CELL for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()

    # Print column letters (A-G for 7 columns)
    letters = string.ascii_uppercase[0:len(board[0])]
    header_row = "  " + "   ".join(letters)
    print(header_row)

    # Print the horizontal border line
    sep = "+" + "---+" * len(board[0])
    for row in range(len(board)):
        print(sep)
        # Cells row
        cells = "| " + " | ".join(board[row]) + " |"
        print(cells)
    print(sep)

def valid_column_input(col_input, board):
    # Check input length and if uppercase A-Z
    if len(col_input) != 1:
        return False
    if col_input not in string.ascii_uppercase[0:len(board[0])]:
        return False
    col_index = ord(col_input) - ord('A')
    # Check if column is full (top row is not empty)
    if board[0][col_index] != EMPTY_CELL:
        return False
    return True

def place_checker(board, checker, col_letter):
    col = ord(col_letter) - ord('A')
    # Place checker at the lowest empty position in the column
    for row in range(len(board) - 1, -1, -1):
        if board[row][col] == EMPTY_CELL:
            board[row][col] = checker
            return row, col
    # Column full, lose turn (should only happen if validation failed)
    return None, None

def check_win(board, checker, last_row, last_col):
    # Directions (row_delta, col_delta)
    directions = [
        (0, 1),   # horizontal right
        (1, 0),   # vertical down
        (1, 1),   # diagonal down-right
        (1, -1)   # diagonal down-left
    ]
    row_count = len(board)
    col_count = len(board[0])

    for dr, dc in directions:
        count = 1

        # check forward direction
        r, c = last_row + dr, last_col + dc
        while 0 <= r < row_count and 0 <= c < col_count and board[r][c] == checker:
            count += 1
            r += dr
            c += dc

        # check backward direction
        r, c = last_row - dr, last_col - dc
        while 0 <= r < row_count and 0 <= c < col_count and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc

        if count >= 4:
            return True
    return False

def board_full(board):
    # If any top cell is empty, board not full yet
    return all(cell != EMPTY_CELL for cell in board[0])

def main():
    board = create_board(ROWS, COLS)
    players = CHECKERS[:NUM_PLAYERS]

    # Randomly choose starting player index
    current_idx = random.randint(0, NUM_PLAYERS - 1)

    print_board(board)

    while True:
        current_player = players[current_idx]
        prompt = f"Player {current_player}, please enter a column: "

        # Validate input until correct or column full (lose turn)
        while True:
            user_input = input(prompt).strip().upper()
            if not valid_column_input(user_input, board):
                # If user input is invalid or column full
                # Check if the reason is that column is full
                col_idx = None
                if len(user_input) == 1 and user_input in string.ascii_uppercase[0:COLS]:
                    col_idx = ord(user_input) - ord('A')
                    if board[0][col_idx] != EMPTY_CELL:
                        # Column full, loses turn (does not ask again)
                        user_input = None
                        break
                print("Invalid input. Please enter a valid column letter of a non-full column.")
            else:
                break

        if user_input is None:
            # Lost turn due to full column
            current_idx = (current_idx + 1) % NUM_PLAYERS
            print_board(board)
            continue

        # Place checker
        last_row, last_col = place_checker(board, current_player, user_input)
        print_board(board)

        # Check win
        if check_win(board, current_player, last_row, last_col):
            print(f"Player {current_player} won!")
            break

        # Check draw
        if board_full(board):
            print("The game is a draw!")
            break

        # Next player
        current_idx = (current_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
