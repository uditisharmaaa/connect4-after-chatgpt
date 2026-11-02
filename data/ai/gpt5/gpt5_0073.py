import os
import random
import string

# Constants (you can change these for testing; submission should be 6x7 and 2 players)
ROWS = 6
COLUMNS = 7  # Max 26
NUM_PLAYERS = 2  # Between 2 and 5

# Player markers in order
MARKERS = ["X", "O", "V", "H", "M"]

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    cols = len(board[0])
    letters = string.ascii_uppercase[:cols]

    # Header
    header = "  " + "   ".join(letters)
    sep = "+" + "+".join(["---"] * cols) + "+"
    print(header)
    print(sep)
    for r in range(len(board)):
        row_str = "|"
        for c in range(cols):
            row_str += " " + board[r][c] + " |"
        print(row_str)
        print(sep)

def get_valid_column_input(cols):
    letters = string.ascii_uppercase[:cols]
    while True:
        user_in = input().strip()
        if len(user_in) != 1:
            print("Invalid input. Please enter a single letter for the column.")
            continue
        ch = user_in.upper()
        if ch not in letters:
            print("Invalid column. Please enter a letter between {} and {}.".format(letters[0], letters[-1]))
            continue
        return letters.index(ch)

def drop_checker(board, col, marker):
    # Place marker in lowest available row in the column
    for row in range(len(board) - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = marker
            return row
    return None  # Column full

def check_win(board, marker):
    rows = len(board)
    cols = len(board[0])

    # Horizontal check
    for r in range(rows):
        for c in range(cols - 3):
            if (board[r][c] == marker and board[r][c+1] == marker and
                board[r][c+2] == marker and board[r][c+3] == marker):
                return True

    # Vertical check
    for c in range(cols):
        for r in range(rows - 3):
            if (board[r][c] == marker and board[r+1][c] == marker and
                board[r+2][c] == marker and board[r+3][c] == marker):
                return True

    # Diagonal down-right
    for r in range(rows - 3):
        for c in range(cols - 3):
            if (board[r][c] == marker and board[r+1][c+1] == marker and
                board[r+2][c+2] == marker and board[r+3][c+3] == marker):
                return True

    # Diagonal up-right
    for r in range(3, rows):
        for c in range(cols - 3):
            if (board[r][c] == marker and board[r-1][c+1] == marker and
                board[r-2][c+2] == marker and board[r-3][c+3] == marker):
                return True

    return False

def check_draw(board):
    # If no spaces in top row, it's full (or we can check all cells)
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == " ":
                return False
    return True

def main():
    # Adjust inputs to constraints
    cols = max(1, min(COLUMNS, 26))
    rows = max(1, ROWS)
    num_players = max(2, min(NUM_PLAYERS, 5))

    players = MARKERS[:num_players]
    board = create_board(rows, cols)

    # Randomly select starting player
    current_player_idx = random.randint(0, num_players - 1)

    # Initial display
    clear_screen()
    print_board(board)

    # Game loop
    while True:
        marker = players[current_player_idx]
        print(f"Player {marker}, please enter a column:")
        col_index = get_valid_column_input(cols)

        placed_row = drop_checker(board, col_index, marker)
        if placed_row is None:
            # Column full: invalid turn, player loses the turn
            clear_screen()
            print_board(board)
            print("Column is full. You lose your turn.")
            # Next player's turn
            current_player_idx = (current_player_idx + 1) % num_players
            # Check draw even if no piece placed (optional but safe)
            if check_draw(board):
                print("The game is a draw!")
                break
            continue

        # After placing, clear and print board
        clear_screen()
        print_board(board)

        # Check for win
        if check_win(board, marker):
            print(f"Player {marker} won!")
            break

        # Check for draw
        if check_draw(board):
            print("The game is a draw!")
            break

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % num_players

if __name__ == "__main__":
    main()
