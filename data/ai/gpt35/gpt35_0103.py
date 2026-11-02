import os
import random
import string

# Constants (submission requires 6 rows x 7 columns, 2 players)
ROWS = 6
COLUMNS = 7
PLAYER_COUNT = 2
WIN_CONDITION = 4
MAX_COLUMNS = 26  # max columns supported

# Checkers for up to 5 players, use only for Player_Count players
CHECKERS = ["X", "O", "V", "H", "M"]

def clear_screen():
    os.system('clear')

def create_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    columns = len(board[0])
    rows = len(board)
    # Print header (A, B, C, ...)
    header = "  "
    for i in range(columns):
        header += "  " + string.ascii_uppercase[i] + " "
    print(header)
    # Print the horizontal separator and rows
    horizontal_line = "+" + "---+" * columns
    for r in range(rows):
        print(horizontal_line)
        row_str = "|"
        for c in range(columns):
            row_str += " " + board[r][c] + " |"
        print(row_str)
    print(horizontal_line)

def pick_random_start_player(count):
    return random.randint(0, count - 1)

def is_valid_column_input(inp, columns):
    if len(inp) != 1:
        return False
    if inp < 'A' or inp >= chr(ord('A') + columns):
        return False
    return True

def get_column_index(inp):
    return ord(inp) - ord('A')

def place_checker(board, col, checker):
    # Place checker in the lowest empty spot of the column, row-wise from bottom up
    for row in reversed(range(len(board))):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    return False  # column full

def board_full(board):
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True

def check_win(board, checker):
    rows = len(board)
    columns = len(board[0])

    # Horizontal check
    for r in range(rows):
        for c in range(columns - WIN_CONDITION + 1):
            if all(board[r][c + i] == checker for i in range(WIN_CONDITION)):
                return True

    # Vertical check
    for c in range(columns):
        for r in range(rows - WIN_CONDITION + 1):
            if all(board[r + i][c] == checker for i in range(WIN_CONDITION)):
                return True

    # Diagonal checks (\ direction)
    for r in range(rows - WIN_CONDITION + 1):
        for c in range(columns - WIN_CONDITION + 1):
            if all(board[r + i][c + i] == checker for i in range(WIN_CONDITION)):
                return True

    # Diagonal checks (/ direction)
    for r in range(WIN_CONDITION - 1, rows):
        for c in range(columns - WIN_CONDITION + 1):
            if all(board[r - i][c + i] == checker for i in range(WIN_CONDITION)):
                return True

    return False

def main():
    # Setup
    rows = ROWS
    columns = COLUMNS
    player_count = PLAYER_COUNT
    board = create_board(rows, columns)
    players = CHECKERS[:player_count]

    current_player_idx = pick_random_start_player(player_count)

    # Print initial board with random player to start
    print_board(board)

    while True:
        player = players[current_player_idx]
        print(f"Player {player}, please enter a column:")

        # Input validation loop
        while True:
            user_input = input().strip().upper()
            if not is_valid_column_input(user_input, columns):
                print(f"Invalid input. Please enter a column letter between A and {chr(ord('A') + columns - 1)}:")
                continue
            col_idx = get_column_index(user_input)
            # Check column full:
            if board[0][col_idx] != " ":
                # Column full, player loses turn (per instructions)
                # Inform player, end turn
                print("Column is full, you lose your turn.")
                break
            else:
                placed = place_checker(board, col_idx, player)
                if not placed:
                    # theoretically unreachable as we just checked full top cell
                    print("Column is full, you lose your turn.")
                break

        # After placing (if placed), print board again
        print_board(board)

        # If placed successfully, check for win
        if board[0][col_idx] != " " or placed:
            if placed and check_win(board, player):
                print(f"Player {player} won!")
                break
            if board_full(board):
                print("The game is a draw!")
                break

        # Switch turns
        current_player_idx = (current_player_idx + 1) % player_count

if __name__ == "__main__":
    main()
