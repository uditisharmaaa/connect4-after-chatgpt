import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
WIN_COUNT = 4
CHECKERS = ["X", "O", "V", "H", "M"]
COLUMN_LABELS = [chr(ord('A') + i) for i in range(COLS)]

def clear_screen():
    os.system('clear')

def create_board():
    # Create a ROWS x COLS board filled with " "
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    # Print column labels
    print("  " + "   ".join(COLUMN_LABELS))
    # Print board rows with horizontal lines
    for row in range(ROWS):
        print("+" + "---+" * COLS)
        row_str = "|"
        for col in range(COLS):
            row_str += " {} |".format(board[row][col])
        print(row_str)
    print("+" + "---+" * COLS)

def get_valid_input(player):
    while True:
        inp = input(f"Player {player}, please enter a column: ").strip().upper()
        if len(inp) != 1:
            # Invalid input length
            continue
        if inp not in COLUMN_LABELS:
            # Invalid column letter
            continue
        col = COLUMN_LABELS.index(inp)
        return col

def place_checker(board, col, checker):
    # Place the checker in the lowest available row in the given column
    for row in range(ROWS-1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row, col
    # Column full
    return -1, -1

def check_direction(board, start_row, start_col, delta_row, delta_col, checker):
    count = 0
    row, col = start_row, start_col
    while 0 <= row < ROWS and 0 <= col < COLS and board[row][col] == checker:
        count += 1
        row += delta_row
        col += delta_col
    return count

def check_win(board, row, col, checker):
    # Check all directions from last placed checker
    # Directions to check: horizontal, vertical, two diagonals
    directions = [ (0,1), (1,0), (1,1), (1,-1) ]
    for dr, dc in directions:
        # Count forwards direction
        forward = check_direction(board, row, col, dr, dc, checker)
        # Count backwards direction (excluding starting cell to avoid double count)
        backward = check_direction(board, row - dr, col - dc, -dr, -dc, checker)
        if forward + backward -1 >= WIN_COUNT:
            return True
    return False

def board_full(board):
    # If there is any " " in top row, board is not full
    for col in range(COLS):
        if board[0][col] == " ":
            return False
    return True

def main():
    board = create_board()
    # Select random player to start
    current_player_index = random.randint(0, PLAYERS - 1)
    print_board(board)

    while True:
        checker = CHECKERS[current_player_index]
        col = get_valid_input(checker)
        row, col_placed = place_checker(board, col, checker)
        if row == -1:
            # Column full, lose turn
            current_player_index = (current_player_index + 1) % PLAYERS
            print_board(board)
            continue
        print_board(board)

        # Check win
        if check_win(board, row, col_placed, checker):
            print(f"Player {checker} won!")
            break
        # Check draw
        if board_full(board):
            print("Game is a draw!")
            break
        # Next player
        current_player_index = (current_player_index + 1) % PLAYERS

if __name__ == "__main__":
    main()
