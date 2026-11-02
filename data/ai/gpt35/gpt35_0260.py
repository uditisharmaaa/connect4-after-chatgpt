import os
import random

# Constants (for submission: board size 6 rows x 7 columns, 2 players)
ROWS = 6
COLUMNS = 7
MIN_PLAYERS = 2
MAX_PLAYERS = 5
NUM_PLAYERS = 2  # Set 2 players for submission

CHECKERS = ['X', 'O', 'V', 'H', 'M']  # max 5 players
WIN_CONDITION = 4

def clear_screen():
    os.system('clear')

def create_board(rows, columns):
    return [[' ' for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    # Print column headers
    header = "  "
    for c in range(len(board[0])):
        header += " " + chr(ord('A') + c) + "  "
    print(header)
    # Print each row with separators
    for r in range(len(board)):
        line = "+"
        for _ in range(len(board[0])):
            line += "---+"
        print(line)
        row_str = "|"
        for c in range(len(board[0])):
            row_str += " " + board[r][c] + " |"
        print(row_str)
    print(line)

def is_valid_column_input(user_input, columns):
    if len(user_input) != 1:
        return False
    if not ('A' <= user_input <= chr(ord('A') + columns -1)):
        return False
    return True

def get_column_index(user_input):
    return ord(user_input) - ord('A')

def find_row_to_place(board, column):
    # Start from bottom row going up to find empty spot
    for r in range(len(board)-1, -1, -1):
        if board[r][column] == ' ':
            return r
    return None  # Column full

def place_checker(board, row, column, checker):
    board[row][column] = checker

def check_win(board, checker):
    rows = len(board)
    columns = len(board[0])
    w = WIN_CONDITION

    # Check horizontal
    for r in range(rows):
        count = 0
        for c in range(columns):
            if board[r][c] == checker:
                count += 1
                if count >= w:
                    return True
            else:
                count = 0

    # Check vertical
    for c in range(columns):
        count = 0
        for r in range(rows):
            if board[r][c] == checker:
                count += 1
                if count >= w:
                    return True
            else:
                count = 0

    # Check diagonal (bottom-left to top-right)
    for r in range(rows - w + 1):
        for c in range(columns - w + 1):
            connected = True
            for i in range(w):
                if board[r + i][c + i] != checker:
                    connected = False
                    break
            if connected:
                return True

    # Check diagonal (top-left to bottom-right)
    for r in range(w - 1, rows):
        for c in range(columns - w + 1):
            connected = True
            for i in range(w):
                if board[r - i][c + i] != checker:
                    connected = False
                    break
            if connected:
                return True

    return False

def check_draw(board):
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == ' ':
                return False
    return True

def select_first_player(num_players):
    return random.randint(0, num_players - 1)

def get_player_input(player_checker, board):
    columns = len(board[0])
    while True:
        user_input = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        if not is_valid_column_input(user_input, columns):
            continue
        col = get_column_index(user_input)
        row = find_row_to_place(board, col)
        if row is None:
            # Column full - player loses turn without input retry
            return None
        return col

def main():
    board = create_board(ROWS, COLUMNS)
    num_players = NUM_PLAYERS
    players = CHECKERS[:num_players]

    current_player_idx = select_first_player(num_players)

    print_board(board)

    while True:
        player_checker = players[current_player_idx]
        col = get_player_input(player_checker, board)
        if col is None:
            # Column full - skip this turn
            current_player_idx = (current_player_idx + 1) % num_players
            print_board(board)
            continue
        row = find_row_to_place(board, col)
        place_checker(board, row, col, player_checker)
        print_board(board)

        if check_win(board, player_checker):
            print(f"Player {player_checker} won!")
            break

        if check_draw(board):
            print("The game is a draw.")
            break

        current_player_idx = (current_player_idx + 1) % num_players

if __name__ == "__main__":
    main()
