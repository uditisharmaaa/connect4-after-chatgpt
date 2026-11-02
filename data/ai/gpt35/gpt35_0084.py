import os
import random

# Constants for board dimensions and number of players
ROWS = 6
COLUMNS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]  # up to 5 players

def clear_screen():
    os.system('clear')

def create_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    # Print column labels
    labels = "  " + "   ".join(chr(ord('A') + i) for i in range(len(board[0])))
    print(labels)
    # Print the board rows with separators
    for row in board:
        print("+" + "---+" * len(row))
        print("| " + " | ".join(row) + " |")
    print("+" + "---+" * len(board[0]))

def random_start_player(num_players):
    return random.randint(0, num_players - 1)

def input_valid(column_input, columns):
    if len(column_input) != 1:
        return False
    c = column_input.upper()
    if c < 'A' or c >= chr(ord('A') + columns):
        return False
    return True

def column_index_from_input(col_input):
    return ord(col_input.upper()) - ord('A')

def place_checker(board, col, checker):
    """
    Places checker in the lowest empty spot of column col.
    Returns True if placed, False if column full.
    """
    for row in reversed(range(len(board))):  # bottom to top
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    return False

def check_win(board, checker):
    rows = len(board)
    cols = len(board[0])
    # Horizontal check
    for r in range(rows):
        for c in range(cols - 3):
            if all(board[r][c+i] == checker for i in range(4)):
                return True
    # Vertical check
    for c in range(cols):
        for r in range(rows - 3):
            if all(board[r+i][c] == checker for i in range(4)):
                return True
    # Diagonal (bottom-left to top-right)
    for r in range(3, rows):
        for c in range(cols - 3):
            if all(board[r - i][c + i] == checker for i in range(4)):
                return True
    # Diagonal (top-left to bottom-right)
    for r in range(rows - 3):
        for c in range(cols - 3):
            if all(board[r + i][c + i] == checker for i in range(4)):
                return True
    return False

def board_full(board):
    return all(cell != " " for row in board for cell in row)

def main():
    board = create_board(ROWS, COLUMNS)
    players_checkers = CHECKERS[:NUM_PLAYERS]
    current_player = random_start_player(NUM_PLAYERS)

    print_board(board)
    print(f"Starting player: Player {players_checkers[current_player]}")

    while True:
        checker = players_checkers[current_player]
        print(f"Player {checker}, please enter a column:")
        user_input = input().strip()
        if not input_valid(user_input, COLUMNS):
            # Invalid input, ask again without losing turn
            continue

        col_idx = column_index_from_input(user_input)
        if not place_checker(board, col_idx, checker):
            # Column full, lose turn
            print(f"Column {user_input.upper()} is full. Player {checker} loses the turn.")
            current_player = (current_player + 1) % NUM_PLAYERS
            print_board(board)
            continue

        print_board(board)

        # Check win
        if check_win(board, checker):
            print(f"Player {checker} won!")
            break

        # Check draw
        if board_full(board):
            print("The game is a draw.")
            break

        # Next player
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
