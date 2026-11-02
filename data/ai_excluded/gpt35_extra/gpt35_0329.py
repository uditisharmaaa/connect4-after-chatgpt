import os
import random

ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]  # Up to 5 players, but we use 2 here
WIN_CONDITION = 4

def clear_screen():
    os.system('clear')

def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    # Print column headers
    headers = "  "
    for c in range(COLS):
        headers += " " + chr(ord('A') + c) + "  "
    print(headers)
    
    # Print rows with separator lines
    line = "+" + "---+" * COLS
    for r in range(ROWS):
        print(line)
        row_str = "|"
        for c in range(COLS):
            row_str += " " + board[r][c] + " |"
        print(row_str)
    print(line)

def valid_column_input(user_input):
    if len(user_input) != 1:
        return False
    col = ord(user_input) - ord('A')
    if col < 0 or col >= COLS:
        return False
    return True

def is_column_full(board, col):
    return board[0][col] != " "

def place_checker(board, col, checker):
    # Place from bottom row going up
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row, col
    # Column full; should not reach here as we check before
    return None

def check_direction(board, row, col, dr, dc, checker):
    count = 0
    r, c = row, col
    while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
        count += 1
        r += dr
        c += dc
    return count

def check_win(board, row, col, checker):
    # Check horizontal (left and right)
    total = 1
    total += check_direction(board, row, col - 1, 0, -1, checker)  # left
    total += check_direction(board, row, col + 1, 0, 1, checker)   # right
    if total >= WIN_CONDITION:
        return True

    # Check vertical (down only, since checkers stack)
    total = 1
    total += check_direction(board, row + 1, col, 1, 0, checker)
    if total >= WIN_CONDITION:
        return True

    # Check diagonal 1 (\)
    total = 1
    total += check_direction(board, row - 1, col - 1, -1, -1, checker)  # up-left
    total += check_direction(board, row + 1, col + 1, 1, 1, checker)    # down-right
    if total >= WIN_CONDITION:
        return True

    # Check diagonal 2 (/)
    total = 1
    total += check_direction(board, row - 1, col + 1, -1, 1, checker)   # up-right
    total += check_direction(board, row + 1, col - 1, 1, -1, checker)   # down-left
    if total >= WIN_CONDITION:
        return True

    return False

def board_full(board):
    for c in range(COLS):
        if board[0][c] == " ":
            return False
    return True

def main():
    board = create_board()
    players_checkers = CHECKERS[:PLAYERS]
    current_player_index = random.randint(0, PLAYERS - 1)
    
    print_board(board)

    while True:
        checker = players_checkers[current_player_index]
        print(f"Player {checker}, please enter a column:")
        user_input = input().strip().upper()

        # Input validation
        if not valid_column_input(user_input):
            print("Invalid input. Please enter a valid column letter (A-G).")
            continue

        col = ord(user_input) - ord('A')
        if is_column_full(board, col):
            # Turn is lost
            print(f"Column {user_input} is full. Player {checker} loses the turn.")
            # Switch player
            current_player_index = (current_player_index + 1) % PLAYERS
            print_board(board)
            continue

        row_col = place_checker(board, col, checker)
        print_board(board)

        if row_col is None:
            # Should not happen due to previous check, but just in case
            print(f"Column {user_input} is full. Player {checker} loses the turn.")
        else:
            row, col_placed = row_col
            if check_win(board, row, col_placed, checker):
                print(f"Player {checker} won!")
                break
            if board_full(board):
                print("The game is a draw.")
                break

        current_player_index = (current_player_index + 1) % PLAYERS

if __name__ == "__main__":
    main()
