import os
import random

# CONSTANTS
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_COUNT = 4

def clear_screen():
    os.system('clear')

def create_board(rows=NUM_ROWS, cols=NUM_COLS):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    cols = len(board[0])
    # Print column headers (A, B, C, ...)
    headers = "  " + "   ".join(chr(ord('A') + i) for i in range(cols))
    print(headers)
    # Print each row of the board
    row_line = "+" + "---+" * cols
    for row in board:
        print(row_line)
        row_str = "|"
        for cell in row:
            row_str += " " + cell + " |"
        print(row_str)
    print(row_line)

def get_random_start_player(num_players):
    return random.randint(0, num_players - 1)

def input_valid_column(input_str, board):
    input_str = input_str.strip()
    if len(input_str) != 1:
        return False
    col_char = input_str[0]
    if not ('A' <= col_char <= chr(ord('A') + len(board[0]) - 1)):
        return False
    col_index = ord(col_char) - ord('A')
    # Check if column is not full (there must be at least one empty space)
    if board[0][col_index] != " ":
        # column full
        return False
    return True

def place_checker(board, col_index, checker):
    """
    Places checker in given column index.
    Checker falls to lowest available row in that column.
    Returns True if placed successfully, False if column full.
    """
    rows = len(board)
    for r in range(rows - 1, -1, -1):
        if board[r][col_index] == " ":
            board[r][col_index] = checker
            return True
    return False  # Column full

def check_win(board, checker):
    rows = len(board)
    cols = len(board[0])

    # Horizontal check
    for r in range(rows):
        count = 0
        for c in range(cols):
            if board[r][c] == checker:
                count += 1
                if count == WIN_COUNT:
                    return True
            else:
                count = 0

    # Vertical check
    for c in range(cols):
        count = 0
        for r in range(rows):
            if board[r][c] == checker:
                count += 1
                if count == WIN_COUNT:
                    return True
            else:
                count = 0

    # Diagonal checks
    # Top-left to bottom-right
    for r in range(rows - WIN_COUNT + 1):
        for c in range(cols - WIN_COUNT + 1):
            win = True
            for i in range(WIN_COUNT):
                if board[r + i][c + i] != checker:
                    win = False
                    break
            if win:
                return True

    # Bottom-left to top-right
    for r in range(WIN_COUNT - 1, rows):
        for c in range(cols - WIN_COUNT + 1):
            win = True
            for i in range(WIN_COUNT):
                if board[r - i][c + i] != checker:
                    win = False
                    break
            if win:
                return True

    return False

def check_draw(board):
    # Draw if top row has no empty spaces in any column
    return all(cell != " " for cell in board[0])

def main():
    board = create_board()
    players = CHECKERS[:NUM_PLAYERS]

    current_player = get_random_start_player(NUM_PLAYERS)

    print_board(board)

    while True:
        checker = players[current_player]
        prompt = f"Player {checker}, please enter a column: "
        while True:
            col_input = input(prompt).strip().upper()
            if input_valid_column(col_input, board):
                col_index = ord(col_input) - ord('A')
                placed = place_checker(board, col_index, checker)
                if not placed:
                    # Column full - player loses turn
                    # Informing player as per spec (turn is lost)
                    break
                else:
                    break
            else:
                # Invalid input, ask again (do not lose turn)
                pass

        print_board(board)

        # Check win
        if placed and check_win(board, checker):
            print(f"Player {checker} won!")
            break

        # Check draw
        if check_draw(board):
            print("The game is a draw.")
            break

        # Next player turn
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
