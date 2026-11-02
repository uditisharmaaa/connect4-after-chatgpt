import os
import random
import string

# Constants for board size and player setup
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    col_labels = list(string.ascii_uppercase[:len(board[0])])
    print('  ' + '   '.join(col_labels))
    print('+' + '---+' * len(col_labels))
    for row in board:
        row_str = '| ' + ' | '.join(row) + ' |'
        print(row_str)
        print('+' + '---+' * len(col_labels))

def get_valid_column(board, prompt):
    valid_cols = list(string.ascii_uppercase[:len(board[0])])
    while True:
        col_input = input(prompt).strip().upper()
        if len(col_input) != 1 or col_input not in valid_cols:
            print("Invalid column! Please choose a valid column letter.")
            continue
        col_idx = valid_cols.index(col_input)
        if board[0][col_idx] != ' ':
            print("Column is full! You lose your turn.")
            return None
        return col_idx

def drop_checker(board, col, checker):
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = checker
            return board.index(row)
    return None

def check_win(board, last_row, last_col, checker):
    directions = [
        (0, 1),  # horizontal
        (1, 0),  # vertical
        (1, 1),  # diagonal down-right
        (1, -1)  # diagonal up-right
    ]
    for dr, dc in directions:
        count = 1
        # Check in the positive direction
        r, c = last_row + dr, last_col + dc
        while 0 <= r < NUM_ROWS and 0 <= c < NUM_COLS and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # Check in the negative direction
        r, c = last_row - dr, last_col - dc
        while 0 <= r < NUM_ROWS and 0 <= c < NUM_COLS and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        if count >= 4:
            return True
    return False

def board_full(board):
    for cell in board[0]:
        if cell == ' ':
            return False
    return True

def main():
    board = create_board(NUM_ROWS, NUM_COLS)
    player_checkers = CHECKERS[:NUM_PLAYERS]
    player = random.randint(0, NUM_PLAYERS - 1)
    print_board(board)
    print(f"Player {player_checkers[player]} starts!")
    input("Press Enter to start...")  # To show initial board before clearing

    while True:
        print_board(board)
        checker = player_checkers[player]
        prompt = f"Player {checker}, please enter a column: "
        col = get_valid_column(board, prompt)
        if col is None:
            # Column is full, turn lost
            player = (player + 1) % NUM_PLAYERS
            continue
        row = drop_checker(board, col, checker)
        if check_win(board, row, col, checker):
            print_board(board)
            print(f"Player {checker} won!")
            break
        if board_full(board):
            print_board(board)
            print("It's a draw!")
            break
        player = (player + 1) % NUM_PLAYERS

if __name__ == '__main__':
    main()
