import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
MIN_PLAYERS = 2
PLAYERS = 2  # Set number of players here (between MIN_PLAYERS and MAX_PLAYERS)
CHECKERS = ["X", "O", "V", "H", "M"]  # Player checkers
WIN_LENGTH = 4

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    # Create a board filled with spaces
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    # Print column headers A, B, C...
    header = "  " + "   ".join(chr(ord('A') + i) for i in range(len(board[0])))
    print(header)
    # Print line separator
    line = "+---" * len(board[0]) + "+"
    for row in board:
        print(line)
        # Print board row with vertical separators and spaces around checker
        print("| " + " | ".join(row) + " |")
    print(line)

def input_column(player_checker, board):
    cols = len(board[0])
    while True:
        col_input = input(f"Player {player_checker}, please enter a column: ").strip()
        if len(col_input) != 1:
            # Invalid length
            continue
        col_char = col_input.upper()
        if not ('A' <= col_char < chr(ord('A') + cols)):
            # Outside board range
            continue
        col_index = ord(col_char) - ord('A')
        # Check if column is full
        if board[0][col_index] != " ":
            # Column full: player loses turn
            return -1
        return col_index

def place_checker(board, col, checker):
    # Place checker in lowest empty cell in col
    for row in range(len(board) - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row, col
    return -1, -1  # Should not happen if checked before

def check_direction(board, start_row, start_col, dr, dc, checker):
    count = 0
    r, c = start_row, start_col
    while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == checker:
        count += 1
        r += dr
        c += dc
    return count

def check_win(board, last_row, last_col, checker):
    # Check horizontal, vertical, and two diagonals for 4 in a row

    directions = [ 
        [(0, -1), (0, 1)],   # left and right horizontal
        [(-1, 0), (1, 0)],   # up and down vertical
        [(-1, -1), (1, 1)],  # diagonal top-left to bottom-right
        [(-1, 1), (1, -1)]   # diagonal top-right to bottom-left
    ]

    for direction_pair in directions:
        count = 1  # count includes last placed checker
        for dr, dc in direction_pair:
            count += check_direction(board, last_row + dr, last_col + dc, dr, dc, checker)
        if count >= WIN_LENGTH:
            return True
    return False

def board_full(board):
    for col in range(len(board[0])):
        if board[0][col] == " ":
            return False
    return True

def main():
    # Prepare game
    num_players = PLAYERS
    if num_players < MIN_PLAYERS or num_players > MAX_PLAYERS:
        num_players = MIN_PLAYERS
    checkers = CHECKERS[:num_players]
    board = create_board(ROWS, COLUMNS)
    current_player_index = random.randint(0, num_players -1)

    print_board(board)

    while True:
        checker = checkers[current_player_index]
        col = input_column(checker, board)
        if col == -1:
            # Column full - lose turn
            # Inform and skip turn
            # Do not change board
            current_player_index = (current_player_index + 1) % num_players
            continue

        last_row, last_col = place_checker(board, col, checker)
        print_board(board)
        if check_win(board, last_row, last_col, checker):
            print(f"Player {checker} won!")
            break
        if board_full(board):
            print("The game is a draw!")
            break
        current_player_index = (current_player_index + 1) % num_players

if __name__ == "__main__":
    main()
