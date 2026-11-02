import os
import random
import string

# Constants
ROWS = 6
COLS = 7
MIN_PLAYERS = 2
MAX_PLAYERS = 5
PLAYERS = MIN_PLAYERS  # Set number of players here (2 for submission)
CHECKERS = ["X", "O", "V", "H", "M"]  # Up to 5 players
WIN_COUNT = 4

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    cols = len(board[0])
    col_labels = [string.ascii_uppercase[i] for i in range(cols)]
    print("  " + "   ".join(col_labels))
    print("+" + "---+" * cols)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * cols)

def valid_input(col, cols):
    if len(col) != 1:
        return False
    if col not in string.ascii_uppercase[:cols]:
        return False
    return True

def drop_checker(board, col_idx, checker):
    # Place checker in lowest empty space in column col_idx
    for row_rev in range(len(board)-1, -1, -1):
        if board[row_rev][col_idx] == " ":
            board[row_rev][col_idx] = checker
            return row_rev
    return -1  # Column full

def check_win(board, row, col, checker):
    rows = len(board)
    cols = len(board[0])

    def count_dir(r_step, c_step):
        count = 1
        # Check forward direction
        r, c = row + r_step, col + c_step
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r += r_step
            c += c_step
        # Check backward direction
        r, c = row - r_step, col - c_step
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r -= r_step
            c -= c_step
        return count

    # Horizontal check
    if count_dir(0,1) >= WIN_COUNT:
        return True
    # Vertical check
    if count_dir(1,0) >= WIN_COUNT:
        return True
    # Diagonal bottom-left to top-right check
    if count_dir(1,1) >= WIN_COUNT:
        return True
    # Diagonal top-left to bottom-right check
    if count_dir(1,-1) >= WIN_COUNT:
        return True

    return False

def board_full(board):
    return all(cell != " " for row in board for cell in row)

def main():
    # Setup
    players = PLAYERS
    checkers = CHECKERS[:players]
    rows = ROWS
    cols = COLS

    board = create_board(rows, cols)
    current_player_idx = random.randrange(players)

    while True:
        clear_screen()
        print_board(board)
        current_checker = checkers[current_player_idx]
        prompt = f"Player {current_checker}, please enter a column: "
        # Ask for valid input
        valid_col_input = False
        while not valid_col_input:
            col = input(prompt).strip().upper()
            if not valid_input(col, cols):
                continue  # invalid input letter or length, ask again
            col_idx = string.ascii_uppercase.index(col)
            # Check if column full
            if board[0][col_idx] != " ":
                # Turn lost due to full column
                valid_col_input = True
                row_placed = -1
                break
            row_placed = drop_checker(board, col_idx, current_checker)
            if row_placed == -1:
                # Should not happen due to above check, but handle just in case
                valid_col_input = True
                break
            valid_col_input = True

        if row_placed == -1:
            # Full column, turn lost
            # Move to next player
            current_player_idx = (current_player_idx + 1) % players
            continue

        # Check win
        if check_win(board, row_placed, col_idx, current_checker):
            clear_screen()
            print_board(board)
            print(f"Player {current_checker} won!")
            break

        # Check draw
        if board_full(board):
            clear_screen()
            print_board(board)
            print("The game is a draw!")
            break

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % players

if __name__ == "__main__":
    main()
