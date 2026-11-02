import os
import random

# Constants (change NUM_PLAYERS between 2 and 5)
ROWS = 6
COLS = 7
COLUMN_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']
NUM_PLAYERS = 2  # set between 2 and 5

def clear_screen():
    os.system('clear')

def make_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board, current_player):
    clear_screen()
    print("Connect 4 - {} players: {}".format(NUM_PLAYERS, ' '.join(PLAYER_SYMBOLS[:NUM_PLAYERS])))
    print("Current player: {}".format(current_player))
    print('  ' + ' '.join(COLUMN_LABELS))
    for r in range(ROWS):
        row_str = []
        for c in range(COLS):
            row_str.append(board[r][c])
        print(str(r+1) + ' ' + ' '.join(row_str))
    print()

def find_drop_row(board, col_idx):
    for r in range(ROWS - 1, -1, -1):
        if board[r][col_idx] == ' ':
            return r
    return None

def get_move(current_player):
    while True:
        move = input("Player {} - choose column (A-G): ".format(current_player)).strip().upper()
        if len(move) != 1 or move not in COLUMN_LABELS:
            print("Invalid input. Please enter a letter A-G.")
            continue
        return COLUMN_LABELS.index(move)

def in_bounds(r, c):
    return 0 <= r < ROWS and 0 <= c < COLS

def check_win_from(board, r, c, dr, dc):
    sym = board[r][c]
    if sym == ' ':
        return False
    for k in range(1, 4):
        rr = r + dr * k
        cc = c + dc * k
        if not in_bounds(rr, cc) or board[rr][cc] != sym:
            return False
    return True

def check_win(board):
    directions = [
        (0, 1),   # right
        (1, 0),   # down
        (1, 1),   # down-right
        (1, -1),  # down-left
    ]
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == ' ':
                continue
            for dr, dc in directions:
                if check_win_from(board, r, c, dr, dc):
                    return board[r][c]
    return None

def check_draw(board):
    for c in range(COLS):
        if board[0][c] == ' ':
            return False
    return True

def main():
    if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
        print("NUM_PLAYERS must be between 2 and 5.")
        return

    symbols = PLAYER_SYMBOLS[:NUM_PLAYERS]
    board = make_board()

    # Pick random first player
    current_idx = random.randrange(NUM_PLAYERS)
    current_player = symbols[current_idx]

    while True:
        print_board(board, current_player)
        col_idx = get_move(current_player)

        drop_row = find_drop_row(board, col_idx)
        if drop_row is None:
            print("Column {} is full. Try another.".format(COLUMN_LABELS[col_idx]))
            input("Press Enter to continue...")
            continue

        board[drop_row][col_idx] = current_player

        winner = check_win(board)
        if winner is not None:
            print_board(board, current_player)
            print("Player {} wins!".format(winner))
            break

        if check_draw(board):
            print_board(board, current_player)
            print("It's a draw!")
            break

        # Next player's turn
        current_idx = (current_idx + 1) % NUM_PLAYERS
        current_player = symbols[current_idx]

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nGame interrupted.")
