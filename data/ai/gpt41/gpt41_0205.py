import os
import random
import string

# --- Constants ---
ROWS = 6
COLS = 7     # max 26
PLAYERS = 2  # 2-5
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def clear_screen():
    os.system('clear')

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    col_labels = '  ' + '   '.join(string.ascii_uppercase[:COLS])
    sep = '+' + '---+' * COLS
    print(col_labels)
    for row in board:
        print(sep)
        print('|' + '|'.join(f' {c} ' for c in row) + '|')
    print(sep)

def get_valid_column_input(board):
    while True:
        col = input("Please enter a column: ").strip().upper()
        if len(col) != 1 or col not in string.ascii_uppercase[:COLS]:
            print("Invalid input. Please enter a valid column letter.")
            continue
        c = ord(col) - ord('A')
        if board[0][c] != ' ':
            print("Column is full. You lose your turn.")
            return None
        return c

def place_checker(board, col, checker):
    for row in reversed(range(ROWS)):
        if board[row][col] == ' ':
            board[row][col] = checker
            return row, col

def is_winner(board, row, col, checker):
    def count_dir(r_step, c_step):
        count = 0
        r, c = row + r_step, col + c_step
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
            count += 1
            r += r_step
            c += c_step
        return count

    directions = [(0,1), (1,0), (1,1), (1,-1)]
    for dr, dc in directions:
        count = 1 + count_dir(dr, dc) + count_dir(-dr, -dc)
        if count >= 4:
            return True
    return False

def is_draw(board):
    return all(board[0][c] != ' ' for c in range(COLS))

def main():
    board = create_board()
    player_order = random.randint(0, PLAYERS-1)
    print_board(board)
    current = player_order
    player_syms = CHECKERS[:PLAYERS]
    move_count = 0

    while True:
        print(f"Player {player_syms[current]},", end=' ')
        col = get_valid_column_input(board)
        if col is None:
            # Column full, lose turn
            current = (current + 1) % PLAYERS
            continue
        row, col = place_checker(board, col, player_syms[current])
        move_count += 1
        print_board(board)
        if is_winner(board, row, col, player_syms[current]):
            print(f"Player {player_syms[current]} won!")
            break
        if is_draw(board):
            print("It's a draw!")
            break
        current = (current + 1) % PLAYERS

if __name__ == "__main__":
    main()
