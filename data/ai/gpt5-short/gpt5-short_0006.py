import os
import random

# Configuration constants
NUM_ROWS = 6
NUM_COLS = 7
COLUMN_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']  # up to 5 players
NUM_PLAYERS = 2  # set between 2 and 5

CONNECT_N = 4  # number in a row needed to win

def clear_screen():
    os.system('clear')  # as requested

def create_board():
    board = []
    for _ in range(NUM_ROWS):
        row = []
        for _ in range(NUM_COLS):
            row.append(' ')
        board.append(row)
    return board

def print_board(board, players, current_player_index):
    clear_screen()
    print("Connect 4 - {} players: {}".format(len(players), ' '.join(players)))
    print("Current player: {}".format(players[current_player_index]))
    print()
    # Column labels
    print("  " + " ".join(COLUMN_LABELS))
    # Board rows
    for r in range(NUM_ROWS):
        line = []
        for c in range(NUM_COLS):
            line.append(board[r][c])
        print("| " + " ".join(line))
    print()

def get_column_index_from_input(s):
    s = s.strip().upper()
    if s in COLUMN_LABELS:
        return COLUMN_LABELS.index(s)
    return -1

def column_has_space(board, col):
    return board[0][col] == ' '

def drop_piece(board, col, symbol):
    # Drop from bottom up
    for r in range(NUM_ROWS - 1, -1, -1):
        if board[r][col] == ' ':
            board[r][col] = symbol
            return r, col
    return -1, -1  # should not happen if checked before

def in_bounds(r, c):
    return 0 <= r < NUM_ROWS and 0 <= c < NUM_COLS

def count_in_direction(board, r, c, dr, dc, symbol):
    count = 0
    rr = r
    cc = c
    while in_bounds(rr, cc) and board[rr][cc] == symbol:
        count += 1
        rr += dr
        cc += dc
    return count

def is_winning_move(board, r, c, symbol):
    # Check 4 directions: horizontal, vertical, diag down-right, diag up-right
    directions = [(0, 1), (1, 0), (1, 1), (-1, 1)]
    for dr, dc in directions:
        # Count both ways from the last placed piece
        total = 1
        total += count_in_direction(board, r + dr, c + dc, dr, dc, symbol)
        total += count_in_direction(board, r - dr, c - dc, -dr, -dc, symbol)
        if total >= CONNECT_N:
            return True
    return False

def is_draw(board):
    for c in range(NUM_COLS):
        if board[0][c] == ' ':
            return False
    return True

def validate_settings():
    if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
        print("NUM_PLAYERS must be between 2 and 5.")
        return False
    if NUM_PLAYERS > len(PLAYER_SYMBOLS):
        print("Not enough player symbols provided.")
        return False
    if len(COLUMN_LABELS) != NUM_COLS:
        print("COLUMN_LABELS length must equal NUM_COLS.")
        return False
    return True

def get_valid_move(board, player_symbol):
    while True:
        user_in = input("Player {} - choose a column (A-G) or Q to quit: ".format(player_symbol)).strip().upper()
        if user_in == 'Q':
            return -1
        col = get_column_index_from_input(user_in)
        if col == -1:
            print("Invalid column. Enter a letter A-G.")
            continue
        if not column_has_space(board, col):
            print("Column {} is full. Choose another.".format(COLUMN_LABELS[col]))
            continue
        return col

def main():
    if not validate_settings():
        return

    players = PLAYER_SYMBOLS[:NUM_PLAYERS]
    board = create_board()

    # Random first player
    current_player_index = random.randrange(NUM_PLAYERS)

    while True:
        print_board(board, players, current_player_index)
        col = get_valid_move(board, players[current_player_index])
        if col == -1:
            print("Game ended by player.")
            break

        r, c = drop_piece(board, col, players[current_player_index])

        # Check win
        if is_winning_move(board, r, c, players[current_player_index]):
            print_board(board, players, current_player_index)
            print("Player {} wins!".format(players[current_player_index]))
            break

        # Check draw
        if is_draw(board):
            print_board(board, players, current_player_index)
            print("It's a draw!")
            break

        # Next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
