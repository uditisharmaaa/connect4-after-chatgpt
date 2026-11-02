import os
import random
import string

# Constants (changeable, but submit with these values)
ROWS = 6
COLS = 7  # Max 26
NUM_PLAYERS = 2  # between 2 and 5

PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def clear_and_print_board(board):
    os.system('clear')
    cols = len(board[0])
    # Header letters
    letters = string.ascii_uppercase[:cols]
    header = "  " + "   ".join(letters)
    print(header)
    # Top border
    print("+---" * cols + "+")
    # Rows
    for r in range(len(board)):
        row_str = "|"
        for c in range(cols):
            row_str += " " + board[r][c] + " |"
        print(row_str)
        print("+---" * cols + "+")

def get_players(num_players):
    return PLAYER_SYMBOLS[:num_players]

def column_from_input(user_input, cols):
    if len(user_input) != 1:
        return None
    ch = user_input.upper()
    letters = string.ascii_uppercase[:cols]
    if ch in letters:
        return letters.index(ch)
    return None

def drop_checker(board, col, symbol):
    # Place at lowest empty in column. Return row index or None if column full.
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = symbol
            return r
    return None

def in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols

def check_winner(board, symbol):
    rows = len(board)
    cols = len(board[0])
    needed = 4
    directions = [
        (0, 1),   # horizontal
        (1, 0),   # vertical
        (1, 1),   # diag down-right
        (1, -1),  # diag down-left
    ]
    for r in range(rows):
        for c in range(cols):
            if board[r][c] != symbol:
                continue
            for dr, dc in directions:
                count = 0
                rr, cc = r, c
                while in_bounds(rr, cc, rows, cols) and board[rr][cc] == symbol:
                    count += 1
                    if count == needed:
                        return True
                    rr += dr
                    cc += dc
    return False

def is_draw(board):
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == " ":
                return False
    return True

def main():
    rows = ROWS
    cols = COLS
    num_players = NUM_PLAYERS
    num_players = max(2, min(5, num_players))
    cols = max(1, min(26, cols))

    board = create_board(rows, cols)
    players = get_players(num_players)

    # Random starting player index
    current_index = random.randrange(num_players)

    # Show initial board
    clear_and_print_board(board)

    while True:
        # Check draw before turn (board might be full due to previous moves)
        if is_draw(board):
            print("It's a draw!")
            break

        current_player = players[current_index]
        print(f"Player {current_player}, please enter a column:")
        # Input validation loop (for input format and range only)
        while True:
            user_in = input().strip()
            col = column_from_input(user_in, cols)
            if col is None:
                print("Invalid input. Please enter a valid column letter (e.g., A, B, C).")
                continue
            break

        # Try to drop checker
        row_placed = drop_checker(board, col, current_player)
        if row_placed is None:
            # Column full: turn is lost
            clear_and_print_board(board)
            print(f"Column {string.ascii_uppercase[col]} is full. Player {current_player} loses the turn.")
            # Next player's turn
            current_index = (current_index + 1) % num_players
            continue

        # Successful placement: update board and check for win/draw
        clear_and_print_board(board)

        if check_winner(board, current_player):
            print(f"Player {current_player} won!")
            break

        if is_draw(board):
            print("It's a draw!")
            break

        # Next player's turn
        current_index = (current_index + 1) % num_players

if __name__ == "__main__":
    main()
