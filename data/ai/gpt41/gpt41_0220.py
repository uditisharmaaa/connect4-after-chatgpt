import os
import random
import string

# ----- Constants -----
ROWS = 6  # Board rows
COLUMNS = 7  # Board columns (max 26)
NUM_PLAYERS = 2  # Number of players (2-5)
CHECKERS = ["X", "O", "V", "H", "M"]  # Checkers for up to 5 players

EMPTY_CELL = " "
WIN_COUNT = 4  # Number of checkers in a row to win

# ----- Functions -----

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[EMPTY_CELL for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    cols = len(board[0])
    header = "  " + "   ".join(string.ascii_uppercase[:cols])
    print(header)
    print("+" + "---+" * cols)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * cols)

def is_valid_column(input_col, cols):
    return (
        len(input_col) == 1 and
        input_col in string.ascii_uppercase[:cols]
    )

def is_column_full(board, col):
    return all(board[row][col] != EMPTY_CELL for row in range(len(board)))

def get_lowest_empty_row(board, col):
    for row in range(len(board) - 1, -1, -1):
        if board[row][col] == EMPTY_CELL:
            return row
    return None

def place_checker(board, col, checker):
    row = get_lowest_empty_row(board, col)
    if row is not None:
        board[row][col] = checker
        return True, row, col
    else:
        return False, None, None

def check_win(board, row, col, checker):
    return any(
        count_consecutive(board, row, col, dr, dc, checker) >= WIN_COUNT
        for dr, dc in [ (0, 1), (1, 0), (1, 1), (1, -1)]
    )

def count_consecutive(board, row, col, dr, dc, checker):
    count = 1
    # Forward direction
    r, c = row + dr, col + dc
    while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == checker:
        count += 1
        r += dr
        c += dc
    # Backward direction
    r, c = row - dr, col - dc
    while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == checker:
        count += 1
        r -= dr
        c -= dc
    return count

def check_draw(board):
    return all(board[0][col] != EMPTY_CELL for col in range(len(board[0])))

def input_prompt(player_checker, cols):
    while True:
        user_input = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        if not is_valid_column(user_input, cols):
            print("Invalid input. Please enter a valid column letter.")
            continue
        col = ord(user_input) - ord('A')
        return col

def main():
    # --- Initialization
    board = create_board(ROWS, COLUMNS)
    player_checkers = CHECKERS[:NUM_PLAYERS]
    player_names = [f"{checker}" for checker in player_checkers]
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)

    print_board(board)
    print(f"Player {player_checkers[current_player_idx]} starts!\nPress Enter to begin.")
    input()

    while True:
        print_board(board)
        player_checker = player_checkers[current_player_idx]
        cols = len(board[0])
        col = input_prompt(player_checker, cols)

        # Try placing checker
        if is_column_full(board, col):
            print("Column is full. You lose your turn.")
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            input("Press Enter to continue...")
            continue

        valid_move, row, col = place_checker(board, col, player_checker)
        if valid_move:
            if check_win(board, row, col, player_checker):
                print_board(board)
                print(f"Player {player_checker} won!")
                break
            elif check_draw(board):
                print_board(board)
                print("The game is a draw!")
                break
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
        else:
            print("This column is already full! You lose your turn.")
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            input("Press Enter to continue...")

if __name__ == '__main__':
    main()
