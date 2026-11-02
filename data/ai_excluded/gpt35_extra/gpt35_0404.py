import os
import random

# CONSTANTS
ROWS = 6
COLS = 7
MAX_COLS = 26
MIN_PLAYERS = 2
MAX_PLAYERS = 5
WIN_SEQUENCE = 4
PLAYERS_CHECKERS = ["X", "O", "V", "H", "M"]

def clear_screen():
    os.system('clear')

def create_board(rows=ROWS, cols=COLS):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    cols = len(board[0])
    # Print column headers
    header = "  "
    for i in range(cols):
        header += "  " + chr(ord('A') + i) + " "
    print(header)
    # Print board rows
    for r in range(len(board)):
        print("+" + "---+" * cols)
        row_str = "|"
        for c in range(cols):
            row_str += " " + board[r][c] + " |"
        print(row_str)
    print("+" + "---+" * cols)

def get_valid_input(player_checker, board):
    cols = len(board[0])
    valid_cols = [chr(ord('A') + i) for i in range(cols)]
    while True:
        user_input = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        if len(user_input) != 1:
            # Invalid length
            continue
        if user_input not in valid_cols:
            # Not a valid column letter
            continue
        col_index = ord(user_input) - ord('A')
        # Check if column full
        if board[0][col_index] != " ":
            # Column full: player loses turn
            return None
        return col_index

def place_checker(board, col_index, checker):
    # Place checker in lowest available row in col_index
    for row in range(len(board)-1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = checker
            return row, col_index
    # Column full (should not reach here if checked earlier)
    return None, None

def check_win(board, checker):
    rows = len(board)
    cols = len(board[0])

    # Check horizontal
    for r in range(rows):
        count = 0
        for c in range(cols):
            if board[r][c] == checker:
                count += 1
                if count == WIN_SEQUENCE:
                    return True
            else:
                count = 0

    # Check vertical
    for c in range(cols):
        count = 0
        for r in range(rows):
            if board[r][c] == checker:
                count += 1
                if count == WIN_SEQUENCE:
                    return True
            else:
                count = 0

    # Check diagonal (top-left to bottom-right)
    for r in range(rows - WIN_SEQUENCE + 1):
        for c in range(cols - WIN_SEQUENCE + 1):
            if all(board[r + i][c + i] == checker for i in range(WIN_SEQUENCE)):
                return True

    # Check diagonal (bottom-left to top-right)
    for r in range(WIN_SEQUENCE - 1, rows):
        for c in range(cols - WIN_SEQUENCE + 1):
            if all(board[r - i][c + i] == checker for i in range(WIN_SEQUENCE)):
                return True

    return False

def check_draw(board):
    # If top row has no space left, board is full
    return all(cell != " " for cell in board[0])

def main():
    # Setup game
    rows = ROWS
    cols = COLS
    players_count = 2
    players_checkers = PLAYERS_CHECKERS[:players_count]

    # Create board and choose first player randomly
    board = create_board(rows, cols)
    current_player_idx = random.randint(0, players_count - 1)
    print_board(board)

    while True:
        checker = players_checkers[current_player_idx]
        col_index = get_valid_input(checker, board)
        if col_index is None:
            # Column full, lose turn
            print(f"Column full. Player {checker} loses turn!")
            input("Press Enter to continue...")
        else:
            place_checker(board, col_index, checker)
            print_board(board)
            if check_win(board, checker):
                print(f"Player {checker} won!")
                break
            if check_draw(board):
                print("Game ended in a draw!")
                break
        current_player_idx = (current_player_idx + 1) % players_count

if __name__ == "__main__":
    main()
