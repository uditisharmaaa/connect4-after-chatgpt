import os
import random
import sys

# Constants - can be changed to support different board sizes and number of players
ROWS = 6
COLS = 7
MAX_PLAYERS = 5
NUM_PLAYERS = 2  # must be between 2 and MAX_PLAYERS
WIN_COUNT = 4
CHECKERS = ["X", "O", "V", "H", "M"]

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    """Create a board filled with spaces."""
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    cols = len(board[0])
    # Print column letters
    header = "  " + "   ".join(chr(ord('A') + i) for i in range(cols))
    print(header)
    # Print rows separated by lines
    horizontal_line = "+" + "---+" * cols
    for row in board:
        print(horizontal_line)
        print("| " + " | ".join(row) + " |")
    print(horizontal_line)

def is_valid_column(col_char, cols):
    """Check if the input character is a valid column letter."""
    if len(col_char) != 1:
        return False
    col = ord(col_char) - ord('A')
    return 0 <= col < cols

def get_column_index(col_char):
    """Convert column letter to index."""
    return ord(col_char) - ord('A')

def column_full(board, col):
    """Check if the column is full."""
    return board[0][col] != " "

def place_checker(board, col, checker):
    """Place checker in the specified column if possible.
       Returns True if placed, False if column full."""
    for row in range(len(board)-1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    return False

def check_winner(board, checker):
    rows = len(board)
    cols = len(board[0])

    # Check horizontal
    for r in range(rows):
        for c in range(cols - WIN_COUNT + 1):
            if all(board[r][c+i] == checker for i in range(WIN_COUNT)):
                return True

    # Check vertical
    for c in range(cols):
        for r in range(rows - WIN_COUNT + 1):
            if all(board[r+i][c] == checker for i in range(WIN_COUNT)):
                return True

    # Check diagonal (down-right)
    for r in range(rows - WIN_COUNT + 1):
        for c in range(cols - WIN_COUNT + 1):
            if all(board[r+i][c+i] == checker for i in range(WIN_COUNT)):
                return True

    # Check diagonal (up-right)
    for r in range(WIN_COUNT - 1, rows):
        for c in range(cols - WIN_COUNT + 1):
            if all(board[r-i][c+i] == checker for i in range(WIN_COUNT)):
                return True

    return False

def board_full(board):
    """Returns True if no empty spaces exist on the board."""
    return all(cell != " " for row in board for cell in row)

def select_first_player(num_players):
    """Randomly select an index of the first player."""
    return random.randint(0, num_players-1)

def get_player_input(player_checker, cols):
    """Prompt the player to enter a valid column letter."""
    while True:
        user_input = input(f"Player {player_checker}, please enter a column: ").upper().strip()
        if not is_valid_column(user_input, cols):
            print(f"Invalid input. Please enter a letter from A to {chr(ord('A')+cols-1)}.")
            continue
        col = get_column_index(user_input)
        return col

def main():
    if NUM_PLAYERS < 2 or NUM_PLAYERS > MAX_PLAYERS:
        print(f"Number of players must be between 2 and {MAX_PLAYERS}.")
        sys.exit(1)

    board = create_board(ROWS, COLS)
    players = CHECKERS[:NUM_PLAYERS]
    current_player_idx = select_first_player(NUM_PLAYERS)

    print_board(board)

    while True:
        player_checker = players[current_player_idx]
        col = get_player_input(player_checker, COLS)

        if column_full(board, col):
            print(f"Column {chr(ord('A')+col)} is full. You lose your turn.")
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            print_board(board)
            continue

        place_checker(board, col, player_checker)
        print_board(board)

        if check_winner(board, player_checker):
            print(f"Player {player_checker} won!")
            break

        if board_full(board):
            print("The game is a draw!")
            break

        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
