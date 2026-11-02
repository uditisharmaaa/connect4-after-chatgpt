import os
import random

ROWS = 6
COLS = 7
PLAYERS = 2
WIN_CONDITION = 4
CHECKERS = ["X", "O", "V", "H", "M"]

def clear_screen():
    os.system('clear')

def create_board():
    board = []
    for r in range(ROWS):
        row = []
        for c in range(COLS):
            row.append(" ")
        board.append(row)
    return board

def print_board(board):
    clear_screen()
    letters = []
    for i in range(COLS):
        letters.append(chr(ord('A') + i))
    print("  " + "   ".join(letters))
    for r in range(ROWS):
        print("+" + "---+" * COLS)
        line = "|"
        for c in range(COLS):
            line += " " + board[r][c] + " |"
        print(line)
    print("+" + "---+" * COLS)

def get_next_player(current):
    return (current + 1) % PLAYERS

def is_valid_column(col_char):
    if len(col_char) != 1:
        return False
    col_char = col_char.upper()
    if col_char < 'A' or col_char >= chr(ord('A') + COLS):
        return False
    return True

def get_column_index(col_char):
    return ord(col_char.upper()) - ord('A')

def place_checker(board, col, checker):
    # Place checker from bottom row upwards
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return r
    # Column full
    return -1

def check_win(board, checker, row, col):
    # Directions: horizontal, vertical, diagonal /, diagonal \
    directions = [
        (0, 1),  # horizontal right
        (1, 0),  # vertical down
        (1, 1),  # diagonal down-right
        (1, -1)  # diagonal down-left
    ]
    for dr, dc in directions:
        count = 1
        # check one direction
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # check opposite direction
        r, c = row - dr, col - dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        if count >= WIN_CONDITION:
            return True
    return False

def is_draw(board):
    for c in range(COLS):
        if board[0][c] == " ":
            return False
    return True

def main():
    board = create_board()
    players = CHECKERS[:PLAYERS]
    current_player = random.randint(0, PLAYERS -1)
    print_board(board)
    while True:
        checker = players[current_player]
        print(f"Player {checker}, please enter a column:")
        col_char = input().strip()
        while not is_valid_column(col_char):
            print("Invalid input. Please enter a valid column letter:")
            col_char = input().strip()
        col = get_column_index(col_char)
        pos = place_checker(board, col, checker)
        if pos == -1:
            # column full, lose turn
            current_player = get_next_player(current_player)
            print_board(board)
            continue
        print_board(board)
        if check_win(board, checker, pos, col):
            print(f"Player {checker} won!")
            break
        if is_draw(board):
            print("It's a draw!")
            break
        current_player = get_next_player(current_player)

if __name__ == "__main__":
    main()
