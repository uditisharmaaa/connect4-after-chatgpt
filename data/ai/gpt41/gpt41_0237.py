import os
import random
import string

# --- Constants ---
ROWS = 6
COLS = 7
MAX_COLS = 26
PLAYERS = 2                    # Can be changed up to 5
CHECKERS = ['X', 'O', 'V', 'H', 'M'][:PLAYERS]
EMPTY = ' '

def clear_screen():
    os.system('clear')

def create_board():
    return [[EMPTY for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    headers = "  " + "   ".join(string.ascii_uppercase[:COLS])
    print(headers)
    print("+" + "---+" * COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)

def get_valid_columns(board):
    return [i for i in range(COLS) if board[0][i] == EMPTY]

def input_column(board, player):
    valid_columns = get_valid_columns(board)
    valid_letters = [string.ascii_uppercase[c] for c in valid_columns]
    while True:
        col_input = input(f"Player {CHECKERS[player]}, please enter a column: ").strip().upper()
        if len(col_input) == 1 and col_input in string.ascii_uppercase[:COLS]:
            col = string.ascii_uppercase.index(col_input)
            if col in valid_columns:
                return col
            else:
                print("Column full! You lose your turn.")
                return None
        else:
            print(f"Invalid input. Choose one of: {', '.join(valid_letters)}.")

def place_checker(board, col, checker):
    for row in reversed(board):
        if row[col] == EMPTY:
            row[col] = checker
            return board.index(row), col
    return None

def is_winner(board, row, col, checker):
    directions = [(0,1), (1,0), (1,1), (1,-1)]  # horiz, vert, diag\, diag/
    for dr, dc in directions:
        count = 1
        # forward
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # backward
        r, c = row - dr, col - dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        if count >= 4:
            return True
    return False

def is_draw(board):
    return all(cell != EMPTY for cell in board[0])

def main():
    board = create_board()
    curr_player = random.randint(0, PLAYERS - 1)
    print_board(board)

    while True:
        col = input_column(board, curr_player)
        if col is not None:
            row, col = place_checker(board, col, CHECKERS[curr_player])
            print_board(board)
            if is_winner(board, row, col, CHECKERS[curr_player]):
                print(f"Player {CHECKERS[curr_player]} won!")
                break
            if is_draw(board):
                print("Game is a draw!")
                break
        else:
            print_board(board)
        curr_player = (curr_player + 1) % PLAYERS

if __name__ == '__main__':
    main()
