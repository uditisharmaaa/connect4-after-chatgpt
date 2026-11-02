import os
import random
import string

# Constants (for submission: 6 rows, 7 columns, 2 players)
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]  # Support up to 5 players, here only 2 used

def clear_screen():
    os.system('clear')


def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    clear_screen()
    # Print column headers (A, B, ..., max 26 columns)
    col_labels = string.ascii_uppercase[:len(board[0])]
    print("  " + "   ".join(col_labels))
    print("+---" * len(board[0]) + "+")
    for row in board:
        line = "| " + " | ".join(row) + " |"
        print(line)
        print("+---" * len(board[0]) + "+")


def get_valid_column_input(board, player_checkers, current_player_idx):
    valid_cols = string.ascii_uppercase[:len(board[0])]
    while True:
        inp = input(f"Player {player_checkers[current_player_idx]}, please enter a column: ").strip().upper()
        if len(inp) != 1 or inp not in valid_cols:
            # Invalid character or out of range
            print("Invalid input. Please enter a valid column letter.")
            continue
        col = valid_cols.index(inp)
        # Check if column is full:
        if board[0][col] != " ":
            # Column full => turn lost
            print(f"Column {inp} is full. You lose your turn.")
            return None
        return col


def place_checker(board, col, checker):
    # Place checker in lowest empty cell in column
    for row_idx in range(len(board)-1, -1, -1):
        if board[row_idx][col] == " ":
            board[row_idx][col] = checker
            return row_idx, col
    # Column full - should not reach here since checked before
    return None


def check_win(board, checker, r, c):
    rows = len(board)
    cols = len(board[0])
    directions = [
        (0, 1),   # horizontal right
        (1, 0),   # vertical down
        (1, 1),   # diagonal down-right
        (1, -1),  # diagonal down-left
    ]

    for dr, dc in directions:
        count = 1
        # Check in positive direction
        rr, cc = r + dr, c + dc
        while 0 <= rr < rows and 0 <= cc < cols and board[rr][cc] == checker:
            count += 1
            rr += dr
            cc += dc

        # Check in negative direction
        rr, cc = r - dr, c - dc
        while 0 <= rr < rows and 0 <= cc < cols and board[rr][cc] == checker:
            count += 1
            rr -= dr
            cc -= dc

        if count >= 4:
            return True
    return False


def check_draw(board):
    # Draw if no top row cells are empty
    return all(cell != " " for cell in board[0])


def main():
    board = create_board(ROWS, COLS)
    player_checkers = CHECKERS[:PLAYERS]
    current_player_idx = random.randint(0, PLAYERS - 1)
    print_board(board)

    while True:
        col = get_valid_column_input(board, player_checkers, current_player_idx)
        if col is not None:
            r, c = place_checker(board, col, player_checkers[current_player_idx])
            print_board(board)
            # Check win after placing checker
            if check_win(board, player_checkers[current_player_idx], r, c):
                print(f"Player {player_checkers[current_player_idx]} won!")
                break
            if check_draw(board):
                print("The game is a draw.")
                break
        else:
            # Turn lost due to full column
            print_board(board)

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % PLAYERS


if __name__ == "__main__":
    main()
