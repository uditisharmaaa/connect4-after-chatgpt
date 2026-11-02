import os
import random
import string

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']  # max 5 players

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    cols = len(board[0])
    # Print column headers
    header = '  '
    for i in range(cols):
        header += '  ' + string.ascii_uppercase[i] + ' '
    print(header)
    print('+' + '---+'*cols)
    for row in board:
        line = '|'
        for cell in row:
            line += f' {cell} |'
        print(line)
        print('+' + '---+'*cols)

def input_valid(column_str, cols):
    if len(column_str) != 1:
        return False
    if column_str not in string.ascii_uppercase[:cols]:
        return False
    return True

def place_checker(board, col_idx, checker):
    # Place checker in column col_idx, in the lowest empty row
    for r in range(len(board)-1, -1, -1):
        if board[r][col_idx] == ' ':
            board[r][col_idx] = checker
            return r, col_idx
    return -1, -1  # column full

def check_four_in_a_row(board, r, c, checker):
    ROWS = len(board)
    COLS = len(board[0])
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
        if count >= 4:
            return True
    return False

def board_full(board):
    for c in range(len(board[0])):
        if board[0][c] == ' ':
            return False
    return True

def main():
    board = create_board(ROWS, COLS)
    players_checkers = CHECKERS[:PLAYERS]
    current_player_idx = random.randint(0, PLAYERS-1)

    print_board(board)

    while True:
        checker = players_checkers[current_player_idx]
        prompt = f"Player {checker}, please enter a column: "
        
        # Input validation loop
        while True:
            user_input = input(prompt).strip().upper()
            if not input_valid(user_input, COLS):
                # invalid input, ask again
                continue
            col = string.ascii_uppercase.index(user_input)
            row_placed, col_placed = place_checker(board, col, checker)
            if row_placed == -1:
                # column full, player loses turn
                break
            else:
                # successful placement
                break

        # if could not place because full column, skip checking win and next player
        if row_placed == -1:
            print_board(board)
            current_player_idx = (current_player_idx + 1) % PLAYERS
            continue

        print_board(board)

        # Check win
        if check_four_in_a_row(board, row_placed, col_placed, checker):
            print(f"Player {checker} won!")
            return

        # Check draw
        if board_full(board):
            print("It's a draw!")
            return

        current_player_idx = (current_player_idx + 1) % PLAYERS


if __name__ == "__main__":
    main()
