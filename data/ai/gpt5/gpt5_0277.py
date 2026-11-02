import os
import random
import string

# Constants (submission requires 6x7 and 2 players)
ROWS = 6
COLS = 7  # max 26
NUM_PLAYERS = 2  # between 2 and 5
CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]

def clear():
    os.system('clear')

def create_board(r, c):
    return [[" " for _ in range(c)] for _ in range(r)]

def print_board(board):
    cols = len(board[0])
    labels = list(string.ascii_uppercase[:cols])
    # Header
    print("  " + "   ".join(labels))
    print("+" + "---+" * cols)
    # Rows
    for r in range(len(board)):
        print("| " + " | ".join(board[r]) + " |")
        print("+" + "---+" * cols)

def drop_checker(board, col, sym):
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = sym
            return r
    return None  # column full

def in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols

def check_win(board, sym):
    rows, cols = len(board), len(board[0])
    directions = [(0,1),(1,0),(1,1),(1,-1)]
    for r in range(rows):
        for c in range(cols):
            if board[r][c] != sym:
                continue
            for dr, dc in directions:
                count = 1
                rr, cc = r + dr, c + dc
                while count < 4 and in_bounds(rr, cc, rows, cols) and board[rr][cc] == sym:
                    count += 1
                    rr += dr
                    cc += dc
                if count == 4:
                    return True
    return False

def board_full(board):
    return all(cell != " " for row in board for cell in row)

def get_column_input(cols, player_sym):
    labels = string.ascii_uppercase[:cols]
    while True:
        inp = input(f"Player {player_sym}, please enter a column: ").strip()
        if len(inp) != 1 or inp.upper() not in labels:
            print("Invalid input. Enter a single column letter within range.")
            continue
        return labels.index(inp.upper())

def main():
    if not (2 <= NUM_PLAYERS <= 5):
        raise ValueError("NUM_PLAYERS must be between 2 and 5.")
    if not (1 <= COLS <= 26):
        raise ValueError("COLS must be between 1 and 26.")

    board = create_board(ROWS, COLS)
    current = random.randrange(NUM_PLAYERS)

    clear()
    print_board(board)

    while True:
        sym = CHECKERS[current]
        col = get_column_input(COLS, sym)
        row = drop_checker(board, col, sym)
        if row is None:
            # Column full, lose turn
            clear()
            print_board(board)
            print(f"Column {string.ascii_uppercase[col]} is full. Player {sym} loses the turn.")
            current = (current + 1) % NUM_PLAYERS
            continue

        clear()
        print_board(board)

        if check_win(board, sym):
            print(f"Player {sym} won!")
            break
        if board_full(board):
            print("Game is a draw.")
            break

        current = (current + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
