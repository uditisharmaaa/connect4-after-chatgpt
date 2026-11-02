import os
import random
import sys

# Constants
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
MIN_PLAYERS = 2
PLAYERS = 2  # must be 2 for submission
CHECKERS = ["X", "O", "V", "H", "M"]

def clear_screen():
    os.system('clear')

def create_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    # Print column headers A...G
    header = "  "
    for i in range(len(board[0])):
        header += "  " + chr(ord('A') + i) + " "
    print(header)
    print("+" + "---+" * len(board[0]))
    for row in board:
        line = "|"
        for cell in row:
            line += " " + cell + " |"
        print(line)
        print("+" + "---+" * len(board[0]))

def choose_starting_player(num_players):
    return random.randint(0, num_players - 1)

def is_valid_column(col, columns):
    return len(col) == 1 and 'A' <= col <= chr(ord('A') + columns - 1)

def get_column_index(col):
    return ord(col) - ord('A')

def place_checker(board, col_idx, checker):
    # place checker in lowest empty spot in column
    for row_idx in range(len(board)-1, -1, -1):
        if board[row_idx][col_idx] == " ":
            board[row_idx][col_idx] = checker
            return row_idx, col_idx
    return None  # column full

def check_direction(board, start_row, start_col, delta_row, delta_col, checker):
    count = 0
    row = start_row
    col = start_col
    while 0 <= row < len(board) and 0 <= col < len(board[0]) and board[row][col] == checker:
        count += 1
        row += delta_row
        col += delta_col
    return count

def check_win(board, row, col, checker):
    # Check all 4 directions for 4 in a row
    directions = [
        (0, 1),  # horizontal right
        (1, 0),  # vertical down
        (1, 1),  # diagonal down-right
        (1, -1), # diagonal down-left
    ]
    for dr, dc in directions:
        # count backwards in opposite direction
        count = check_direction(board, row, col, -dr, -dc, checker) - 1
        # plus forwards in direction
        count += check_direction(board, row, col, dr, dc, checker)
        if count >= 4:
            return True
    return False

def board_full(board):
    # If top row has no empty spaces, board is full
    return all(cell != " " for cell in board[0])

def next_player(current, num_players):
    return (current + 1) % num_players

def main():
    # Setup
    rows = ROWS
    columns = COLUMNS
    num_players = PLAYERS
    checkers = CHECKERS[:num_players]
    board = create_board(rows, columns)
    current_player = choose_starting_player(num_players)
    
    print_board(board)

    while True:
        player_checker = checkers[current_player]
        print(f"Player {player_checker}, please enter a column:")
        user_input = input().strip().upper()

        if not is_valid_column(user_input, columns):
            # Invalid input, ask again (turn not lost)
            continue

        col_idx = get_column_index(user_input)
        placed = place_checker(board, col_idx, player_checker)
        if placed is None:
            # Column full, lose turn
            current_player = next_player(current_player, num_players)
            print_board(board)
            continue

        print_board(board)
        r, c = placed
        if check_win(board, r, c, player_checker):
            print(f"Player {player_checker} won!")
            break
        if board_full(board):
            print("The game is a draw!")
            break
        current_player = next_player(current_player, num_players)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit()
