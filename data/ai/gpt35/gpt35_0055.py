import os
import random
import string

# ===== Constants =====
ROWS = 6
COLUMNS = 7
MAX_COLUMNS = 26
MIN_PLAYERS = 2
MAX_PLAYERS = 5
WIN_LENGTH = 4
PLAYERS = ["X", "O", "V", "H", "M"]

# ===== Functions =====

def clear_screen():
    os.system('clear')

def create_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    columns = len(board[0])
    # Print column headers
    header = "  "
    for i in range(columns):
        header += f"  {string.ascii_uppercase[i]} "
    print(header)
    # Print board rows + separators
    separator = "+" + "---+" * columns
    for row in board:
        print(separator)
        line = "|"
        for cell in row:
            line += f" {cell} |"
        print(line)
    print(separator)

def is_valid_column(col_char, columns):
    if len(col_char) != 1:
        return False
    col_char = col_char.upper()
    if col_char < 'A' or col_char >= chr(ord('A') + columns):
        return False
    return True

def column_index(col_char):
    return ord(col_char.upper()) - ord('A')

def place_checker(board, col, checker):
    """
    Place checker in given column (0-based index).
    Returns True if placed successfully, False if column full.
    """
    for row in range(len(board)-1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    return False  # Column full

def is_full(board):
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True

def check_win(board, checker):
    rows = len(board)
    cols = len(board[0])

    # Horizontal check
    for r in range(rows):
        for c in range(cols - WIN_LENGTH + 1):
            if all(board[r][c+i] == checker for i in range(WIN_LENGTH)):
                return True

    # Vertical check
    for c in range(cols):
        for r in range(rows - WIN_LENGTH + 1):
            if all(board[r+i][c] == checker for i in range(WIN_LENGTH)):
                return True

    # Diagonal \ check
    for r in range(rows - WIN_LENGTH + 1):
        for c in range(cols - WIN_LENGTH + 1):
            if all(board[r+i][c+i] == checker for i in range(WIN_LENGTH)):
                return True

    # Diagonal / check
    for r in range(WIN_LENGTH - 1, rows):
        for c in range(cols - WIN_LENGTH + 1):
            if all(board[r-i][c+i] == checker for i in range(WIN_LENGTH)):
                return True

    return False

def main():
    # Settings for submission requirements:
    rows = ROWS
    columns = COLUMNS
    num_players = 2
    players = PLAYERS[:num_players]

    # Check for max columns constraint (<=26)
    if columns > MAX_COLUMNS:
        raise ValueError(f"Max columns allowed is {MAX_COLUMNS}")

    board = create_board(rows, columns)
    
    # Randomly select starting player index
    current_player_idx = random.randint(0, num_players-1)

    print_board(board)

    # Game loop
    while True:
        current_player_checker = players[current_player_idx]
        # Input loop
        while True:
            user_input = input(f"Player {current_player_checker}, please enter a column: ").strip()
            if not is_valid_column(user_input, columns):
                continue  # Reprompt on invalid input
            col = column_index(user_input)
            # Check if column full before placing
            if board[0][col] != " ":
                # Column full -> player loses turn
                break  # Exit input loop but skip placing
            placed = place_checker(board, col, current_player_checker)
            if placed:
                break  # Valid move placed
            else:
                # theoretically can't get here because of column full check above,
                # but just in case ask input again
                continue

        print_board(board)

        # If player placed a checker check for win and draw
        if board[0][col] != " " or not (board[0][col] == " "): # placed successful or column was full
            # If they placed (not lost turn)
            # If move was valid (placed a checker)
            if placed:
                if check_win(board, current_player_checker):
                    print(f"Player {current_player_checker} won!")
                    break
                if is_full(board):
                    print("The game is a draw!")
                    break

        # Next player's turn unless player lost their turn by full column
        current_player_idx = (current_player_idx + 1) % num_players

if __name__ == "__main__":
    main()
