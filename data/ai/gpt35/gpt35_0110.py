import os
import random

# Constants for the game
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]  # Up to 5 players
WIN_LEN = 4

def clear_screen():
    os.system('clear')

def create_board():
    board = []
    for _ in range(ROWS):
        board.append([" "] * COLS)
    return board

def print_board(board):
    clear_screen()
    # Print column headers
    header = "  "
    for i in range(COLS):
        header += chr(ord('A') + i) + "   "
    print(header)
    # Print board rows
    for r in range(ROWS):
        line = "+"
        for _ in range(COLS):
            line += "---+"
        print(line)
        row_str = "|"
        for c in range(COLS):
            row_str += " " + board[r][c] + " |"
        print(row_str)
    print("+" + "---+" * COLS)

def is_valid_column(col_char):
    if len(col_char) != 1:
        return False
    col = ord(col_char) - ord('A')
    return 0 <= col < COLS

def column_full(board, col):
    return board[0][col] != " "

def place_checker(board, col, checker):
    # Place checker in lowest available row in the specified column
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return r, col
    return None  # Column is full; should not happen if checked before

def check_win(board, r, c, checker):
    # Directions: horizontal, vertical, diagonal / and diagonal \
    directions = [
        (0, 1),   # horizontal right
        (1, 0),   # vertical down
        (1, 1),   # diagonal down-right
        (1, -1)   # diagonal down-left
    ]
    for dr, dc in directions:
        count = 1
        # Check forward direction
        rr, cc = r + dr, c + dc
        while 0 <= rr < ROWS and 0 <= cc < COLS and board[rr][cc] == checker:
            count += 1
            rr += dr
            cc += dc
        # Check backward direction
        rr, cc = r - dr, c - dc
        while 0 <= rr < ROWS and 0 <= cc < COLS and board[rr][cc] == checker:
            count += 1
            rr -= dr
            cc -= dc
        if count >= WIN_LEN:
            return True
    return False

def check_draw(board):
    for c in range(COLS):
        if board[0][c] == " ":
            return False
    return True

def get_player_input(current_player, checker, board):
    while True:
        col_input = input(f"Player {checker}, please enter a column: ").strip().upper()
        if not is_valid_column(col_input):
            # invalid column letter
            continue
        col = ord(col_input) - ord('A')
        if column_full(board, col):
            # column is full, player loses turn as per assignment
            return None
        return col

def main():
    board = create_board()
    players = CHECKERS[:PLAYERS]
    current_player_index = random.randint(0, PLAYERS - 1)
    print_board(board)
    # Game loop
    while True:
        checker = players[current_player_index]
        col = get_player_input(current_player_index, checker, board)
        if col is None:
            # column full, player loses turn
            current_player_index = (current_player_index + 1) % PLAYERS
            continue
        row, col = place_checker(board, col, checker)
        print_board(board)
        if check_win(board, row, col, checker):
            print(f"Player {checker} won!")
            break
        if check_draw(board):
            print("Draw!")
            break
        current_player_index = (current_player_index + 1) % PLAYERS

if __name__ == "__main__":
    main()
