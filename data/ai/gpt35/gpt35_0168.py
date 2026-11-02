import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2  # between 2 and 5
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_COUNT = 4

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    cols = len(board[0])
    # Print column headers
    header = "  " + "   ".join(chr(ord('A') + i) for i in range(cols))
    print(header)
    # Print separator and rows
    sep = "+" + "---+" * cols
    for row in board:
        print(sep)
        row_str = "|" + "|".join(f" {cell} " for cell in row) + "|"
        print(row_str)
    print(sep)

def choose_first_player(num_players):
    return random.randint(0, num_players - 1)

def valid_column_input(col_input, board):
    if len(col_input) != 1:
        return False
    col_char = col_input.upper()
    if not ('A' <= col_char < chr(ord('A') + len(board[0]))):
        return False
    col_index = ord(col_char) - ord('A')
    # Check if the top row of the column is empty (space available)
    return board[0][col_index] == " "

def get_column_index(col_input):
    return ord(col_input.upper()) - ord('A')

def place_checker(board, col_idx, checker):
    """
    Place checker in the correct row (lowest available space in column).
    Return True if placed, False if column full.
    """
    for row in range(len(board)-1, -1, -1):
        if board[row][col_idx] == " ":
            board[row][col_idx] = checker
            return True
    return False  # column full

def check_line_win(line, checker):
    count = 0
    for cell in line:
        if cell == checker:
            count += 1
            if count == WIN_COUNT:
                return True
        else:
            count = 0
    return False

def check_win(board, checker):
    rows = len(board)
    cols = len(board[0])

    # Horizontal check
    for r in range(rows):
        if check_line_win(board[r], checker):
            return True

    # Vertical check
    for c in range(cols):
        col_line = [board[r][c] for r in range(rows)]
        if check_line_win(col_line, checker):
            return True

    # Diagonal checks (both directions)
    # Diagonal down-right (\)
    for r in range(rows - WIN_COUNT + 1):
        for c in range(cols - WIN_COUNT + 1):
            diag = [board[r + i][c + i] for i in range(WIN_COUNT)]
            if all(cell == checker for cell in diag):
                return True

    # Diagonal up-right (/)
    for r in range(WIN_COUNT - 1, rows):
        for c in range(cols - WIN_COUNT + 1):
            diag = [board[r - i][c + i] for i in range(WIN_COUNT)]
            if all(cell == checker for cell in diag):
                return True

    return False

def check_draw(board):
    # If top row is full (no spaces), game is a draw if no winner
    return all(cell != " " for cell in board[0])

def main():
    board = create_board(ROWS, COLUMNS)
    num_players = PLAYERS
    checkers = CHECKERS[:num_players]

    current_player = choose_first_player(num_players)
    print_board(board)

    while True:
        checker = checkers[current_player]
        prompt = f"Player {checker}, please enter a column: "

        # Get valid input
        while True:
            col_input = input(prompt).strip()
            if not valid_column_input(col_input, board):
                # Invalid input - prompt again without losing turn
                continue
            col_idx = get_column_index(col_input)
            # Try to place checker
            placed = place_checker(board, col_idx, checker)
            # If column full, player loses turn (no input retry)
            if not placed:
                break
            else:
                # Successfully placed - break input loop
                break

        print_board(board)

        # If checker was not placed because column full, player loses turn
        if not placed:
            current_player = (current_player + 1) % num_players
            continue

        # Check win
        if check_win(board, checker):
            print(f"Player {checker} won!")
            break

        # Check draw
        if check_draw(board):
            print("The game is a draw.")
            break

        # Next player's turn
        current_player = (current_player + 1) % num_players

if __name__ == "__main__":
    main()
