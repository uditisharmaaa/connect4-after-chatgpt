import os
import random
import string

# Constants
ROWS = 6
COLUMNS = 7
MIN_PLAYERS = 2
MAX_PLAYERS = 5
WIN_COUNT = 4
PLAYERS = ["X", "O", "V", "H", "M"]
NUM_PLAYERS = 2  # Must be between MIN_PLAYERS and MAX_PLAYERS

assert 2 <= NUM_PLAYERS <= 5, f"Number of players must be between {MIN_PLAYERS} and {MAX_PLAYERS}"
assert COLUMNS <= 26, "Maximum number of columns supported is 26"

def clear_screen():
    os.system('clear')

def create_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    # Print column headers
    headers = "  " + "   ".join(string.ascii_uppercase[:COLUMNS])
    print(headers)
    # Print horizontal separator line format
    sep = "+" + ("---+" * COLUMNS)
    for row in board:
        print(sep)
        print("| " + " | ".join(row) + " |")
    print(sep)

def is_valid_column(col_letter):
    if len(col_letter) != 1:
        return False
    col_letter = col_letter.upper()
    if col_letter not in string.ascii_uppercase[:COLUMNS]:
        return False
    return True

def column_to_index(col_letter):
    return string.ascii_uppercase.index(col_letter.upper())

def get_lowest_empty_row(board, col_index):
    for r in reversed(range(ROWS)):
        if board[r][col_index] == " ":
            return r
    return None

def place_checker(board, col_index, checker):
    row = get_lowest_empty_row(board, col_index)
    if row is None:
        return False
    board[row][col_index] = checker
    return True

def check_winner(board, checker):
    # Horizontal check
    for r in range(ROWS):
        count = 0
        for c in range(COLUMNS):
            if board[r][c] == checker:
                count += 1
                if count == WIN_COUNT:
                    return True
            else:
                count = 0

    # Vertical check
    for c in range(COLUMNS):
        count = 0
        for r in range(ROWS):
            if board[r][c] == checker:
                count += 1
                if count == WIN_COUNT:
                    return True
            else:
                count = 0

    # Diagonal (bottom-left to top-right)
    for r in range(ROWS - WIN_COUNT + 1):
        for c in range(COLUMNS - WIN_COUNT + 1):
            if all(board[r + i][c + i] == checker for i in range(WIN_COUNT)):
                return True

    # Diagonal (top-left to bottom-right)
    for r in range(WIN_COUNT - 1, ROWS):
        for c in range(COLUMNS - WIN_COUNT + 1):
            if all(board[r - i][c + i] == checker for i in range(WIN_COUNT)):
                return True

    return False

def board_full(board):
    for r in range(ROWS):
        for c in range(COLUMNS):
            if board[r][c] == " ":
                return False
    return True

def main():
    board = create_board()
    players = PLAYERS[:NUM_PLAYERS]
    # Choose random starting player index
    current_player_index = random.randint(0, NUM_PLAYERS - 1)

    print_board(board)

    while True:
        current_checker = players[current_player_index]
        prompt = f"Player {current_checker}, please enter a column: "
        valid_input = False

        while not valid_input:
            choice = input(prompt).strip().upper()
            if not is_valid_column(choice):
                # Invalid input character or length
                continue
            col_idx = column_to_index(choice)
            # Check if the column is full
            if get_lowest_empty_row(board, col_idx) is None:
                # Column full, player loses turn
                # Just break input loop and lose turn
                valid_input = True
                no_place = True
            else:
                no_place = False
                valid_input = True

        if no_place:
            # Player loses turn, proceed to next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            print_board(board)
            continue

        placed = place_checker(board, col_idx, current_checker)
        print_board(board)

        # Check win
        if check_winner(board, current_checker):
            print(f"Player {current_checker} won!")
            break

        # Check draw
        if board_full(board):
            print("The game is a draw!")
            break

        # Next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
