# Connect 4 (beginner style)
# 6 rows x 7 columns, columns labeled A-G
# 2 to 5 players: X O V H M (set NUM_PLAYERS below)
# Picks a random first player, validates input, checks wins/draws
# Uses os.system('clear') to refresh the screen

import os
import random

# ----- Settings -----
ROWS = 6
COLS = 7
COLUMNS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']
NUM_PLAYERS = 2  # change this to 2, 3, 4, or 5

# ----- Helpers -----

def clear_screen():
    os.system('clear')  # use 'cls' on Windows if needed

def make_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    print("  " + " ".join(COLUMNS))
    for r in range(ROWS):
        row_str = []
        for c in range(COLS):
            row_str.append(board[r][c] if board[r][c] != ' ' else '.')
        print(str(ROWS - r) + " " + " ".join(row_str))
    print()

def col_full(board, col_index):
    return board[0][col_index] != ' '

def drop_piece(board, col_index, symbol):
    # drop from bottom up
    for r in range(ROWS - 1, -1, -1):
        if board[r][col_index] == ' ':
            board[r][col_index] = symbol
            return r, col_index
    return None  # should not happen if checked with col_full

def inside(r, c):
    return 0 <= r < ROWS and 0 <= c < COLS

def check_direction(board, r, c, dr, dc, symbol):
    count = 0
    rr = r
    cc = c
    for _ in range(4):
        if inside(rr, cc) and board[rr][cc] == symbol:
            count += 1
            rr += dr
            cc += dc
        else:
            break
    return count == 4

def check_win(board, symbol):
    # check all cells as potential start for 4-in-a-row
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] != symbol:
                continue
            # Right
            if check_direction(board, r, c, 0, 1, symbol):
                return True
            # Down
            if check_direction(board, r, c, 1, 0, symbol):
                return True
            # Down-right
            if check_direction(board, r, c, 1, 1, symbol):
                return True
            # Down-left
            if check_direction(board, r, c, 1, -1, symbol):
                return True
    return False

def is_draw(board):
    for c in range(COLS):
        if board[0][c] == ' ':
            return False
    return True

def get_player_symbols():
    if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
        print("NUM_PLAYERS must be between 2 and 5. Defaulting to 2.")
        return PLAYER_SYMBOLS[:2]
    return PLAYER_SYMBOLS[:NUM_PLAYERS]

def read_move(current_symbol):
    while True:
        choice = input(f"Player {current_symbol}, choose a column (A-G): ").strip().upper()
        if len(choice) != 1 or choice not in COLUMNS:
            print("Invalid input. Please enter a single letter A-G.")
            continue
        col_index = COLUMNS.index(choice)
        return col_index

# ----- Main game loop -----

def main():
    players = get_player_symbols()
    board = make_board()
    current_idx = random.randrange(len(players))
    winner = None

    while True:
        clear_screen()
        print("Connect 4")
        print(f"Players: {' '.join(players)}  |  Turn: {players[current_idx]}")
        print_board(board)

        # Read and validate move
        col = read_move(players[current_idx])
        if col_full(board, col):
            print("That column is full. Press Enter to try again.")
            input()
            continue

        # Drop piece
        drop_piece(board, col, players[current_idx])

        # Check win
        if check_win(board, players[current_idx]):
            winner = players[current_idx]
            clear_screen()
            print_board(board)
            print(f"Player {winner} wins!")
            break

        # Check draw
        if is_draw(board):
            clear_screen()
            print_board(board)
            print("It's a draw!")
            break

        # Next player
        current_idx = (current_idx + 1) % len(players)

    print("Game over.")

if __name__ == "__main__":
    main()
