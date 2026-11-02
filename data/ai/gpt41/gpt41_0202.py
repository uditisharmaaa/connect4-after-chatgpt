import os
import random
import string

# ------------------ Constants ------------------
BOARD_ROWS = 6           # Number of rows (height)
BOARD_COLS = 7           # Number of columns (width, max 26)
NUM_PLAYERS = 2          # Between 2 and 5

PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]

# ------------------ Functions ------------------

def clear_screen():
    """
    Clear the terminal screen (works in Unix/Linux terminal).
    """
    os.system('clear')

def create_board(rows, cols):
    """
    Create a 2D board initialized with whitespaces.
    """
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """
    Print the entire board with headers and borders (as in the assignment).
    """
    rows = len(board)
    cols = len(board[0])

    # Print column headers (A, B, ...)
    header = "  " + "   ".join(string.ascii_uppercase[:cols])
    print(header)

    # Print top border
    print("+---" * cols + "+")

    for row in board:
        # Print row content
        print("| " + " | ".join(row) + " |")
        # Print row border
        print("+---" * cols + "+")

def get_next_open_row(board, col):
    """
    Return the first open row (from bottom) in column `col`.
    If the column is full, return None.
    """
    for row in reversed(range(len(board))):  # Bottom-up
        if board[row][col] == " ":
            return row
    return None

def is_valid_column(board, col):
    """
    Check if a checker can be placed in column `col`.
    """
    return get_next_open_row(board, col) is not None

def check_win(board, symbol):
    """
    Check if the player with `symbol` has 4 in a row (any direction).
    """
    rows = len(board)
    cols = len(board[0])
    # Directions: (delta_row, delta_col)
    directions = [
        (0, 1),   # horizontal right
        (1, 0),   # vertical down
        (1, 1),   # diagonal down-right
        (1, -1),  # diagonal down-left
    ]

    for row in range(rows):
        for col in range(cols):
            if board[row][col] == symbol:
                for dr, dc in directions:
                    count = 1
                    r, c = row + dr, col + dc
                    while (0 <= r < rows) and (0 <= c < cols) and board[r][c] == symbol:
                        count += 1
                        if count == 4:
                            return True
                        r += dr
                        c += dc
    return False

def is_board_full(board):
    """
    Check if the board has no empty spaces.
    """
    return all(cell != " " for row in board for cell in row)

def input_column(player_symbol, cols):
    """
    Get valid column letter input from the user.
    Only accepts uppercase letters within ['A', ..., chr(ord('A')+cols-1)].
    """
    valid_letters = string.ascii_uppercase[:cols]
    while True:
        inp = input(f"Player {player_symbol}, please enter a column: ").strip().upper()
        if len(inp) != 1 or inp not in valid_letters:
            print("Invalid input. Please enter a valid column letter (e.g., A-G).")
            continue
        col_index = ord(inp) - ord('A')
        return col_index

def main():
    # Game initialization
    board = create_board(BOARD_ROWS, BOARD_COLS)
    players = PLAYER_SYMBOLS[:NUM_PLAYERS]

    # Randomly select first player
    curr_player_index = random.randint(0, NUM_PLAYERS - 1)

    # Initial board print
    clear_screen()
    print_board(board)

    game_won = False
    while not game_won and not is_board_full(board):
        player_symbol = players[curr_player_index]

        col = input_column(player_symbol, BOARD_COLS)

        # Check if column is full before placing
        next_row = get_next_open_row(board, col)
        if next_row is None:
            print("Column is full. You lose your turn.")
            # Lose turn, skip to next player
            curr_player_index = (curr_player_index + 1) % NUM_PLAYERS
            continue

        # Place the checker
        board[next_row][col] = player_symbol

        # Print updated board
        clear_screen()
        print_board(board)

        # Check for win condition
        if check_win(board, player_symbol):
            print(f"Player {player_symbol} won!")
            game_won = True
            break

        # Advance to next player
        curr_player_index = (curr_player_index + 1) % NUM_PLAYERS

    if not game_won:
        print("It's a draw! No more available moves.")

# ------------------ Run Game ------------------

if __name__ == '__main__':
    main()
