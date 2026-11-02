import os
import random
import string

# Constants - set for submission requirements
ROW_COUNT = 6
COLUMN_COUNT = 7
PLAYER_COUNT = 2
CHECKERS = ["X", "O", "V", "H", "M"]  # Max 5 players, use only first PLAYER_COUNT

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    cols = len(board[0])
    # Print column headers A-G
    header = "  "
    for i in range(cols):
        header += "  " + chr(ord('A') + i) + " "
    print(header)
    # Print board with +---+
    line = "+---" * cols + "+"
    for r in range(len(board)):
        print(line)
        row_str = "|"
        for c in range(cols):
            row_str += " " + board[r][c] + " |"
        print(row_str)
    print(line)

def is_valid_column(col_letter, cols):
    if len(col_letter) != 1:
        return False
    if col_letter < 'A' or col_letter >= chr(ord('A') + cols):
        return False
    return True

def get_column_index(col_letter):
    return ord(col_letter) - ord('A')

def is_column_full(board, col_idx):
    return board[0][col_idx] != " "

def place_checker(board, col_idx, checker):
    # Place checker in the lowest empty row in column col_idx
    # Return row index where placed, or -1 if column full
    for row in range(len(board) - 1, -1, -1):
        if board[row][col_idx] == " ":
            board[row][col_idx] = checker
            return row
    return -1

def check_win(board, checker, last_row, last_col):
    rows = len(board)
    cols = len(board[0])
    directions = [
        (0, 1),   # Horizontal right
        (1, 0),   # Vertical down
        (1, 1),   # Diagonal down-right
        (1, -1)   # Diagonal down-left
    ]

    for dr, dc in directions:
        count = 1
        # Check forward direction
        r, c = last_row + dr, last_col + dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # Check backward direction
        r, c = last_row - dr, last_col - dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        if count >= 4:
            return True
    return False

def board_full(board):
    # If top row has any empty space, board not full
    for cell in board[0]:
        if cell == " ":
            return False
    return True

def main():
    board = create_board(ROW_COUNT, COLUMN_COUNT)
    players = CHECKERS[:PLAYER_COUNT]

    current_player_idx = random.randint(0, PLAYER_COUNT - 1)

    print_board(board)

    while True:
        checker = players[current_player_idx]
        prompt = f"Player {checker}, please enter a column: "

        while True:
            user_input = input(prompt).strip().upper()
            if not is_valid_column(user_input, COLUMN_COUNT):
                # Invalid input (not single uppercase letter in A-G)
                continue
            col = get_column_index(user_input)
            if is_column_full(board, col):
                # Column full - player loses turn
                break
            # Place checker
            row_placed = place_checker(board, col, checker)
            if row_placed == -1:
                # Column full case again - lose turn
                break
            else:
                # Successful place
                break

        print_board(board)

        # If player placed checker successfully check for win
        if 'row_placed' in locals() and row_placed != -1:
            if check_win(board, checker, row_placed, col):
                print(f"Player {checker} won!")
                return
            if board_full(board):
                print("The game is a draw.")
                return

        # Next player
        current_player_idx = (current_player_idx + 1) % PLAYER_COUNT
        # Remove row_placed variable for next turn to avoid confusion
        if 'row_placed' in locals():
            del row_placed

if __name__ == "__main__":
    main()
