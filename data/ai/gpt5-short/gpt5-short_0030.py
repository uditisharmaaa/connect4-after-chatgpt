# Connect 4 for Intro CS
# - 6 rows x 7 columns
# - Columns labeled A-G
# - 2 to 5 players allowed, symbols in order: X, O, V, H, M
# - Random first player
# - Validates input
# - Checks wins and draws
# - Clears screen with os.system('clear')
# - Uses only basic Python

import os
import random

# -------- Constants you can change --------
ROWS = 6
COLS = 7
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']  # In this order
NUM_PLAYERS = 2  # Change to 2..5
CLEAR_COMMAND = 'clear'  # Required by the assignment
# -----------------------------------------

def make_board(rows, cols):
    board = []
    for _ in range(rows):
        row = []
        for _ in range(cols):
            row.append(' ')
        board.append(row)
    return board

def clear_screen():
    os.system(CLEAR_COMMAND)

def print_board(board):
    # Column labels
    labels = []
    for i in range(COLS):
        labels.append(chr(ord('A') + i))
    print('  ' + '   '.join(labels))
    print('+---' * COLS + '+')
    for r in range(ROWS):
        line = '|'
        for c in range(COLS):
            line += ' ' + board[r][c] + ' |'
        print(line)
        print('+---' * COLS + '+')

def column_from_input(s):
    if len(s) != 1:
        return -1
    ch = s.upper()
    if ch < 'A' or ch > 'G':
        return -1
    return ord(ch) - ord('A')

def is_column_full(board, col):
    return board[0][col] != ' '

def drop_piece(board, col, symbol):
    # Place from bottom-most empty spot upwards
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == ' ':
            board[r][col] = symbol
            return r, col
    return None  # Should not happen if checked before

def in_bounds(r, c):
    return 0 <= r < ROWS and 0 <= c < COLS

def count_in_direction(board, start_r, start_c, dr, dc, symbol):
    count = 0
    r = start_r
    c = start_c
    while in_bounds(r, c) and board[r][c] == symbol:
        count += 1
        r += dr
        c += dc
    return count

def is_winning_move(board, r, c, symbol):
    # Check all 4 directions by counting both ways
    directions = [
        (0, 1),   # horizontal
        (1, 0),   # vertical
        (1, 1),   # diag down-right
        (1, -1),  # diag down-left
    ]
    for dr, dc in directions:
        # Count current plus both opposite directions, but avoid double counting start
        total = 1
        total += count_line(board, r, c, dr, dc, symbol)
        total += count_line(board, r, c, -dr, -dc, symbol)
        if total >= 4:
            return True
    return False

def count_line(board, r, c, dr, dc, symbol):
    # Count contiguous same symbols starting from next step
    count = 0
    nr = r + dr
    nc = c + dc
    while in_bounds(nr, nc) and board[nr][nc] == symbol:
        count += 1
        nr += dr
        nc += dc
    return count

def is_draw(board):
    # Draw if top row has no spaces
    for c in range(COLS):
        if board[0][c] == ' ':
            return False
    return True

def get_active_players():
    if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
        print("NUM_PLAYERS must be between 2 and 5. Using 2 by default.")
        n = 2
    else:
        n = NUM_PLAYERS
    players = []
    for i in range(n):
        players.append(PLAYER_SYMBOLS[i])
    return players

def prompt_move(player):
    while True:
        s = input("Player " + player + ", choose a column (A-G): ").strip()
        if len(s) == 0:
            print("Please enter a letter A-G.")
            continue
        col = column_from_input(s)
        if col == -1:
            print("Invalid column. Enter a letter A-G.")
            continue
        return col

def main():
    board = make_board(ROWS, COLS)
    players = get_active_players()
    # Pick random first player index
    current_index = random.randint(0, len(players) - 1)

    while True:
        clear_screen()
        print_board(board)
        current_player = players[current_index]

        # Get a valid column
        col = prompt_move(current_player)
        if col < 0 or col >= COLS:
            # Should not happen due to validation
            print("Invalid column index.")
            continue
        if is_column_full(board, col):
            print("That column is full. Press Enter to choose another.")
            input()
            continue

        # Drop the piece
        pos = drop_piece(board, col, current_player)
        r, c = pos[0], pos[1]

        # Check win
        if is_winning_move(board, r, c, current_player):
            clear_screen()
            print_board(board)
            print("Player " + current_player + " wins!")
            break

        # Check draw
        if is_draw(board):
            clear_screen()
            print_board(board)
            print("It's a draw!")
            break

        # Next player
        current_index = (current_index + 1) % len(players)

if __name__ == "__main__":
    main()
