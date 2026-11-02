import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_COLUMNS = 26
MIN_PLAYERS = 2
MAX_PLAYERS = 5
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_LENGTH = 4

def clear_screen():
    os.system('clear')

def create_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    columns = len(board[0])
    # Print column labels
    labels = [chr(ord("A") + i) for i in range(columns)]
    print("  " + "   ".join(labels))
    # Print rows with horizontal dividers
    divider = "+" + "---+" * columns
    for r in range(len(board)):
        print(divider)
        print("| " + " | ".join(board[r]) + " |")
    print(divider)

def is_valid_column(col_char, columns):
    if len(col_char) != 1:
        return False
    if not col_char.isalpha():
        return False
    col_char = col_char.upper()
    return 'A' <= col_char < chr(ord('A') + columns)

def get_column_index(col_char):
    return ord(col_char.upper()) - ord('A')

def place_checker(board, col_index, checker):
    """
    Places the checker in the lowest available slot in the column.
    Returns True if placed, False if column full.
    """
    for row in reversed(range(len(board))):
        if board[row][col_index] == " ":
            board[row][col_index] = checker
            return row, col_index
    return None

def check_win(board, row, col, checker):
    rows = len(board)
    cols = len(board[0])

    def count_direction(dr, dc):
        count = 0
        r, c = row + dr, col + dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        return count

    # directions: horizontal, vertical, \ diagonal, / diagonal
    # We count how many same checkers on each side + the one placed
    directions = [
        (0, 1),  # horizontal right
        (1, 0),  # vertical down
        (1, 1),  # diagonal down-right
        (1, -1), # diagonal down-left
    ]
    for dr, dc in directions:
        count = 1  # current checker
        count += count_direction(dr, dc)
        count += count_direction(-dr, -dc)
        if count >= WIN_LENGTH:
            return True
    return False

def board_full(board):
    return all(cell != " " for row in board for cell in row)

def main():
    # Validate constants
    if not (4 <= ROWS and 4 <= COLUMNS <= MAX_COLUMNS):
        print("Board dimensions must be at least 4x4 and columns max 26.")
        return
    if not (MIN_PLAYERS <= PLAYERS <= MAX_PLAYERS):
        print(f"Number of players must be between {MIN_PLAYERS} and {MAX_PLAYERS}.")
        return

    # Initialize board
    board = create_board(ROWS, COLUMNS)

    # Select players and checkers
    players_checkers = CHECKERS[:PLAYERS]

    # Random start player
    current_player_idx = random.randint(0, PLAYERS -1)

    # Print initial board and indicate starting player
    print_board(board)
    print(f"Player {players_checkers[current_player_idx]}, you start!")

    while True:
        checker = players_checkers[current_player_idx]
        while True:
            col_input = input(f"Player {checker}, please enter a column: ").strip().upper()
            if not is_valid_column(col_input, COLUMNS):
                # Invalid input
                continue
            col_idx = get_column_index(col_input)
            pos = place_checker(board, col_idx, checker)
            if pos is None:
                # Column full -> turn lost
                break
            else:
                # Checker placed
                print_board(board)
                # Check for win
                if check_win(board, pos[0], pos[1], checker):
                    print(f"Player {checker} won!")
                    return
                # Check for draw
                if board_full(board):
                    print("The game is a draw!")
                    return
                break

        # Next player
        current_player_idx = (current_player_idx + 1) % PLAYERS

if __name__ == "__main__":
    main()
