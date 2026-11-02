import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']  # Max 5 players

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    board = [[' ' for _ in range(cols)] for _ in range(rows)]
    return board

def print_board(board):
    clear_screen()
    # Print column letters
    letters = [chr(ord('A') + i) for i in range(COLUMNS)]
    print("  " + "   ".join(letters))
    for r in range(ROWS):
        print("+" + "---+" * COLUMNS)
        row_str = "|"
        for c in range(COLUMNS):
            row_str += " {} |".format(board[r][c])
        print(row_str)
    print("+" + "---+" * COLUMNS)

def is_valid_column(col_char):
    if len(col_char) != 1:
        return False
    if col_char < 'A' or col_char >= chr(ord('A') + COLUMNS):
        return False
    return True

def column_index(col_char):
    return ord(col_char) - ord('A')

def place_checker(board, col, checker):
    # Place checker in the lowest empty spot in column col
    for row in range(ROWS-1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = checker
            return row, col
    return None  # Column full

def check_win(board, row, col, checker):
    # Check horizontally
    count = 0
    for c in range(COLUMNS):
        if board[row][c] == checker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0

    # Check vertically
    count = 0
    for r in range(ROWS):
        if board[r][col] == checker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0

    # Check diagonal (/)
    count = 0
    r_start = row
    c_start = col
    while r_start > 0 and c_start < COLUMNS -1:
        r_start -= 1
        c_start += 1
    r, c = r_start, c_start
    while r < ROWS and c >= 0:
        if board[r][c] == checker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
        r +=1
        c -=1

    # Check diagonal (\)
    count = 0
    r_start = row
    c_start = col
    while r_start > 0 and c_start > 0:
        r_start -= 1
        c_start -= 1
    r, c = r_start, c_start
    while r < ROWS and c < COLUMNS:
        if board[r][c] == checker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
        r +=1
        c +=1

    return False

def board_full(board):
    for c in range(COLUMNS):
        if board[0][c] == ' ':
            return False
    return True

def main():
    board = create_board(ROWS, COLUMNS)
    players_checkers = CHECKERS[:PLAYERS]

    current_player_idx = random.randint(0, PLAYERS -1)

    print_board(board)

    while True:
        checker = players_checkers[current_player_idx]
        # Ask input
        while True:
            user_input = input(f"Player {checker}, please enter a column: ").strip().upper()
            if not is_valid_column(user_input):
                continue
            col = column_index(user_input)
            pos = place_checker(board, col, checker)
            if pos is None:
                # column full, turn lost
                break
            else:
                break

        print_board(board)
        if pos is not None:
            r, c = pos
            if check_win(board, r, c, checker):
                print(f"Player {checker} won!")
                return
            if board_full(board):
                print("Game is a draw!")
                return

        current_player_idx = (current_player_idx + 1) % PLAYERS

if __name__ == "__main__":
    main()
