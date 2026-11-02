import os
import random
import sys

# Constants (submission requires 6 rows x 7 columns and 2 players)
ROWS = 6
COLUMNS = 7  # max 26
NUM_PLAYERS = 2  # between 2 and 5
CHECKERS = ["X", "O", "V", "H", "M"]  # order of player symbols

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    rows = len(board)
    cols = len(board[0])
    # Column headers (A..)
    header = "  " + "   ".join(chr(ord('A') + i) for i in range(cols))
    print(header)
    print("+" + ("---+" * cols))
    for r in range(rows):
        row_str = "|"
        for c in range(cols):
            row_str += " " + board[r][c] + " |"
        print(row_str)
        print("+" + ("---+" * cols))

def get_players(num_players):
    if num_players < 2 or num_players > 5:
        num_players = 2
    return CHECKERS[:num_players]

def is_valid_column_input(s, cols):
    if len(s) != 1 or not s.isalpha() or not s.isupper():
        return False
    idx = ord(s) - ord('A')
    return 0 <= idx < cols

def drop_checker(board, col, checker):
    # Attempt to place checker in lowest empty row of the column
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return r
    return None  # column full

def check_win(board, checker):
    rows = len(board)
    cols = len(board[0])
    needed = 4

    # Horizontal
    for r in range(rows):
        for c in range(cols - needed + 1):
            if all(board[r][c + k] == checker for k in range(needed)):
                return True

    # Vertical
    for c in range(cols):
        for r in range(rows - needed + 1):
            if all(board[r + k][c] == checker for k in range(needed)):
                return True

    # Diagonal down-right
    for r in range(rows - needed + 1):
        for c in range(cols - needed + 1):
            if all(board[r + k][c + k] == checker for k in range(needed)):
                return True

    # Diagonal up-right
    for r in range(needed - 1, rows):
        for c in range(cols - needed + 1):
            if all(board[r - k][c + k] == checker for k in range(needed)):
                return True

    return False

def board_full(board):
    for r in board:
        for cell in r:
            if cell == " ":
                return False
    return True

def main():
    # Safety for columns limit
    if COLUMNS > 26:
        print("Maximum supported columns is 26.")
        return

    board = create_board(ROWS, COLUMNS)
    players = get_players(NUM_PLAYERS)

    # Randomly choose starting player index
    current_player = random.randint(0, len(players) - 1)

    # Initial board print
    clear_screen()
    print_board(board)

    while True:
        # Check draw before asking (all columns filled)
        if board_full(board):
            print("It's a draw!")
            break

        current_checker = players[current_player]
        # Ask for input and validate (letters only, uppercase, within range)
        while True:
            try:
                user_input = input(f"Player {current_checker}, please enter a column: ").strip()
            except EOFError:
                print("\nInput ended. Exiting game.")
                return

            if not is_valid_column_input(user_input, COLUMNS):
                # Invalid input format -> ask again (turn not lost)
                continue
            col = ord(user_input) - ord('A')
            # Try to drop checker
            placed_row = drop_checker(board, col, current_checker)
            if placed_row is None:
                # Column full -> invalid turn, player loses the turn
                clear_screen()
                print_board(board)
                print(f"Column {user_input} is full. Player {current_checker} loses the turn.")
                # Advance to next player and break out of input loop
                current_player = (current_player + 1) % len(players)
                break
            else:
                # Successful placement
                clear_screen()
                print_board(board)

                # Check for win
                if check_win(board, current_checker):
                    print(f"Player {current_checker} won!")
                    return

                # Check for draw
                if board_full(board):
                    print("It's a draw!")
                    return

                # Next player's turn
                current_player = (current_player + 1) % len(players)
                break  # move to next turn

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
