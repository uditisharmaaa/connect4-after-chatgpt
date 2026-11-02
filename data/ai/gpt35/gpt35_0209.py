import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def clear_screen():
    os.system('clear')

def create_board():
    board = [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]
    return board

def print_board(board):
    clear_screen()
    # Print column labels
    labels = '  '
    for i in range(COLUMNS):
        labels += chr(ord('A') + i) + '   '
    print(labels)

    # Print board rows
    for row in board:
        print('+---' * COLUMNS + '+')
        line = '|'
        for cell in row:
            line += ' ' + cell + ' |'
        print(line)
    print('+---' * COLUMNS + '+')

def get_column_index(input_str):
    if len(input_str) != 1:
        return -1
    ch = input_str[0]
    if ch < 'A' or ch > chr(ord('A') + COLUMNS - 1):
        return -1
    return ord(ch) - ord('A')

def column_has_space(board, col):
    return board[0][col] == ' '

def place_checker(board, col, checker):
    # Place checker in the lowest empty row in column col
    for row in range(ROWS-1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = checker
            return row, col
    return -1, -1  # Column full

def check_win(board, checker, row, col):
    # Check horizontal
    count = 0
    for c in range(COLUMNS):
        if board[row][c] == checker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0

    # Check vertical
    count = 0
    for r in range(ROWS):
        if board[r][col] == checker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0

    # Check diagonal /
    count = 0
    start_row = row
    start_col = col
    while start_row > 0 and start_col < COLUMNS -1:
        start_row -=1
        start_col +=1
    r = start_row
    c = start_col
    while r < ROWS and c >=0:
        if board[r][c] == checker:
            count +=1
            if count ==4:
                return True
        else:
            count =0
        r +=1
        c -=1

    # Check diagonal \
    count =0
    start_row = row
    start_col = col
    while start_row >0 and start_col >0:
        start_row -=1
        start_col -=1
    r = start_row
    c = start_col
    while r < ROWS and c < COLUMNS:
        if board[r][c] == checker:
            count +=1
            if count ==4:
                return True
        else:
            count =0
        r +=1
        c +=1

    return False

def is_draw(board):
    for c in range(COLUMNS):
        if board[0][c] == ' ':
            return False
    return True

def main():
    board = create_board()
    players_checkers = CHECKERS[:PLAYERS]

    current_player_index = random.randint(0, PLAYERS-1)

    print_board(board)

    while True:
        checker = players_checkers[current_player_index]
        print(f"Player {checker}, please enter a column:")

        # Input loop
        while True:
            col_input = input().strip().upper()
            col = get_column_index(col_input)
            if col == -1:
                print("Invalid column. Please enter a valid column letter:")
                continue
            if not column_has_space(board, col):
                print("Column full. You lose this turn.")
                # Lose turn, break input loop
                col = -1
            break

        # If column full, lose turn
        if col == -1:
            current_player_index = (current_player_index + 1) % PLAYERS
            print_board(board)
            continue

        row_placed, col_placed = place_checker(board, col, checker)
        print_board(board)

        if check_win(board, checker, row_placed, col_placed):
            print(f"Player {checker} won!")
            break

        if is_draw(board):
            print("The game is a draw.")
            break

        current_player_index = (current_player_index + 1) % PLAYERS

if __name__ == "__main__":
    main()
