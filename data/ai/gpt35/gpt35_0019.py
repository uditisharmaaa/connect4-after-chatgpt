import os
import random
import string

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    cols = len(board[0])
    # Print column labels
    labels = [string.ascii_uppercase[i] for i in range(cols)]
    print("  " + "   ".join(labels))
    # Print the board rows with separators
    for r in range(len(board)):
        print("+" + "---+" * cols)
        row_str = "|"
        for c in range(cols):
            row_str += " " + board[r][c] + " |"
        print(row_str)
    print("+" + "---+" * cols)

def is_valid_column_input(user_input, cols):
    if len(user_input) != 1:
        return False
    column_letter = user_input.upper()
    if column_letter not in string.ascii_uppercase[:cols]:
        return False
    return True

def get_column_index(column_letter):
    return string.ascii_uppercase.index(column_letter)

def place_checker(board, col_idx, checker):
    # place checker in lowest available row in column col_idx
    for row in reversed(range(len(board))):
        if board[row][col_idx] == " ":
            board[row][col_idx] = checker
            return row, col_idx
    return None  # column full

def check_win(board, row, col, checker):
    rows = len(board)
    cols = len(board[0])
    directions = [
        (0, 1),   # horizontal right
        (1, 0),   # vertical down
        (1, 1),   # diagonal down-right
        (1, -1)   # diagonal down-left
    ]
    for dr, dc in directions:
        count = 1
        # check forward direction
        r, c = row + dr, col + dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # check backward direction
        r, c = row - dr, col - dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        if count >= 4:
            return True
    return False

def board_full(board):
    for row in board:
        if " " in row:
            return False
    return True

def main():
    rows = ROWS
    cols = COLUMNS
    players = PLAYERS
    checkers = CHECKERS[:players]

    board = create_board(rows, cols)
    current_player_idx = random.randint(0, players - 1)

    print_board(board)

    while True:
        checker = checkers[current_player_idx]
        print(f"Player {checker}, please enter a column:")

        # input validation loop
        while True:
            user_input = input().strip().upper()
            if not is_valid_column_input(user_input, cols):
                print("Invalid input. Please enter a valid column letter:")
                continue
            col_idx = get_column_index(user_input)
            # check column full
            if board[0][col_idx] != " ":
                # Turn is lost if column full
                print(f"Column {user_input} is full. You lose your turn.")
                placed = None
                break
            placed = place_checker(board, col_idx, checker)
            if placed is not None:
                break
            else:
                # Should not reach here because we checked top row before
                print(f"Column {user_input} is full. You lose your turn.")
                break

        print_board(board)

        if placed:
            r, c = placed
            if check_win(board, r, c, checker):
                print(f"Player {checker} won!")
                break

        if board_full(board):
            print("The game is a draw!")
            break

        current_player_idx = (current_player_idx + 1) % players

if __name__ == "__main__":
    main()
