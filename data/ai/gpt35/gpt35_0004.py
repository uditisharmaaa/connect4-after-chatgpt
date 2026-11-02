import os
import random
import string

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_LENGTH = 4

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    cols = len(board[0])
    # Print column headers
    headers = [string.ascii_uppercase[i] for i in range(cols)]
    print("  " + "   ".join(headers))
    # Print rows with separators
    for r in range(len(board)):
        print("+" + "---+" * cols)
        row_str = "|"
        for c in range(cols):
            row_str += f" {board[r][c]} |"
        print(row_str)
    print("+" + "---+" * cols)

def choose_start_player(num_players):
    return random.randint(0, num_players - 1)

def is_valid_input(user_input, cols):
    if len(user_input) != 1:
        return False
    if not user_input.isalpha():
        return False
    col_index = ord(user_input) - ord('A')
    if col_index < 0 or col_index >= cols:
        return False
    return True

def column_full(board, col):
    return board[0][col] != " "

def place_checker(board, col, checker):
    # Place checker in the lowest available row in column col
    for row in range(len(board)-1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row, col
    # column full
    return None, None

def check_direction(board, row, col, dr, dc, checker):
    count = 0
    r, c = row, col
    while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == checker:
        count += 1
        r += dr
        c += dc
    return count

def check_win(board, row, col, checker):
    # Check all four directions: horizontal, vertical, two diagonals
    directions = [(0,1), (1,0), (1,1), (1,-1)]
    for dr, dc in directions:
        # count checkers on one side including the starting point
        count1 = check_direction(board, row, col, dr, dc, checker)
        # count checkers on the opposite side excluding starting point
        count2 = check_direction(board, row, col, -dr, -dc, checker) - 1
        if count1 + count2 >= WIN_LENGTH:
            return True
    return False

def board_full(board):
    # If top row has any empty space, board not full
    for c in range(len(board[0])):
        if board[0][c] == " ":
            return False
    return True

def get_player_input(player_checker, cols, board):
    while True:
        user_input = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        if not is_valid_input(user_input, cols):
            continue
        col = ord(user_input) - ord('A')
        if column_full(board, col):
            # Player loses turn, no placement
            return None
        return col

def main():
    board = create_board(ROWS, COLS)
    num_players = PLAYERS
    checkers = CHECKERS[:num_players]

    current_player = choose_start_player(num_players)
    print_board(board)

    while True:
        checker = checkers[current_player]
        col = get_player_input(checker, COLS, board)
        if col is None:
            # Column full: lose turn
            current_player = (current_player + 1) % num_players
            print_board(board)
            continue
        row, placed_col = place_checker(board, col, checker)
        print_board(board)

        if check_win(board, row, placed_col, checker):
            print(f"Player {checker} won!")
            break
        if board_full(board):
            print("Game is a draw!")
            break
        current_player = (current_player + 1) % num_players

if __name__ == "__main__":
    main()
