import os
import random
import sys

# Constants
ROWS = 6
COLS = 7
PLAYERS_COUNT = 2

# Checkers order for up to 5 players
CHECKERS = ["X", "O", "V", "H", "M"]

# Ensure valid settings for this submission
if PLAYERS_COUNT < 2 or PLAYERS_COUNT > 5:
    print("Number of players must be between 2 and 5.")
    sys.exit(1)
if COLS > 26:
    print("Number of columns must not exceed 26.")
    sys.exit(1)

def clear_screen():
    os.system('clear')

def create_board():
    # Create a ROWS x COLS board filled with spaces
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    # Print column headers A - G (or appropriate)
    header = "  " + "   ".join(chr(ord('A') + i) for i in range(COLS))
    print(header)
    # Print top border
    print("+" + "---+" * COLS)
    # Print each row
    for row in range(ROWS):
        line = "|"
        for col in range(COLS):
            line += " " + board[row][col] + " |"
        print(line)
        print("+" + "---+" * COLS)

def column_letter_to_index(letter):
    letter = letter.upper()
    idx = ord(letter) - ord('A')
    if 0 <= idx < COLS:
        return idx
    return -1

def is_valid_move(board, col):
    # Check if column is within range and has at least one empty row
    if col < 0 or col >= COLS:
        return False
    return board[0][col] == " "

def place_checker(board, col, checker):
    # Place checker in the lowest empty position in the column
    for row in reversed(range(ROWS)):
        if board[row][col] == " ":
            board[row][col] = checker
            return row, col
    # If column full, return None indicating no placement
    return None, None

def check_win(board, checker, row, col):
    # Directions to check: (row_delta, col_delta)
    directions = [
        (0, 1),  # horizontal right
        (1, 0),  # vertical down
        (1, 1),  # diagonal down-right
        (1, -1)  # diagonal down-left
    ]
    for dr, dc in directions:
        count = 1  # count includes the last placed checker itself
        # Check in the positive direction
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # Check in the negative direction
        r, c = row - dr, col - dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        # Check if 4 or more consecutive
        if count >= 4:
            return True
    return False

def board_full(board):
    # If top row has no free spaces, board is full
    for c in range(COLS):
        if board[0][c] == " ":
            return False
    return True

def get_player_move(board, player_checker):
    while True:
        inp = input(f"Player {player_checker}, please enter a column: ").strip()
        if len(inp) != 1:
            # Invalid length
            continue
        col = column_letter_to_index(inp)
        if col == -1:
            # Not a valid column letter
            continue
        if not is_valid_move(board, col):
            # Column full - player loses turn as per spec
            return -1
        return col

def main():
    board = create_board()
    players = CHECKERS[:PLAYERS_COUNT]

    current_player_idx = random.randint(0, PLAYERS_COUNT - 1)

    print_board(board)

    while True:
        player_checker = players[current_player_idx]
        col = get_player_move(board, player_checker)
        if col == -1:
            # Column full: turn lost (no placement)
            print(f"Column full! Player {player_checker} loses the turn.")
            input("Press Enter to continue...")
            current_player_idx = (current_player_idx + 1) % PLAYERS_COUNT
            print_board(board)
            continue

        row, col_placed = place_checker(board, col, player_checker)
        print_board(board)

        if check_win(board, player_checker, row, col_placed):
            print(f"Player {player_checker} won!")
            break

        if board_full(board):
            print("The game is a draw!")
            break
        current_player_idx = (current_player_idx + 1) % PLAYERS_COUNT

if __name__ == "__main__":
    main()
