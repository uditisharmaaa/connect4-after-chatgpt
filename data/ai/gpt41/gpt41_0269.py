import os
import random

# ===== Constants =====
ROWS = 6
COLS = 7
PLAYER_COUNT = 2  # Set as required, max 5
PLAYER_MARKS = ['X', 'O', 'V', 'H', 'M']
COLUMNS_LABELS = [chr(ord('A') + i) for i in range(COLS)]

# ===== Game Board Initialization =====
def create_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    os.system('clear')
    header = '  ' + '   '.join(COLUMNS_LABELS[:len(board[0])])
    sep = '+' + '---+' * len(board[0])
    print(header)
    print(sep)
    for row in board:
        line = '| ' + ' | '.join(row) + ' |'
        print(line)
        print(sep)

# ===== Input and Move =====
def get_valid_column(board):
    while True:
        col = input("Please enter a column: ").strip().upper()
        if len(col) != 1 or col not in COLUMNS_LABELS[:len(board[0])]:
            print("Invalid column letter. Try again.")
            continue
        col_idx = ord(col) - ord('A')
        # Check if the top position is empty (not full)
        if board[0][col_idx] != ' ':
            print("Column is full! You lose your turn.")
            return None
        return col_idx

def drop_checker(board, col, mark):
    # Go from bottom row up to top, place checker at lowest spot
    for row in reversed(range(len(board))):
        if board[row][col] == ' ':
            board[row][col] = mark
            return row, col

# ===== Win and Draw Check =====
def check_direction(board, row, col, dr, dc, mark):
    count = 0
    for _ in range(4):
        if 0 <= row < len(board) and 0 <= col < len(board[0]) and board[row][col] == mark:
            count += 1
        else:
            break
        row += dr
        col += dc
    return count == 4

def check_win(board, row, col, mark):
    directions = [ (0,1), (1,0), (1,1), (1,-1) ]  # horiz, vert, diag /, diag \
    for dr, dc in directions:
        count = 1
        # Check forward
        r, c = row + dr, col + dc
        while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == mark:
            count += 1
            r += dr
            c += dc
        # Check backward
        r, c = row - dr, col - dc
        while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == mark:
            count += 1
            r -= dr
            c -= dc
        if count >= 4:
            return True
    return False

def is_draw(board):
    return all(cell != ' ' for cell in board[0])

# ===== Main Game Loop =====
def main():
    board = create_board(ROWS, COLS)
    players = PLAYER_MARKS[:PLAYER_COUNT]
    current = random.randint(0, PLAYER_COUNT - 1)

    print_board(board)
    print(f"Player {players[current]} starts!\n")

    while True:
        print_board(board)
        mark = players[current]
        print(f"Player {mark},", end=' ')
        col = get_valid_column(board)
        if col is None:
            current = (current + 1) % PLAYER_COUNT
            continue
        row, col = drop_checker(board, col, mark)
        if check_win(board, row, col, mark):
            print_board(board)
            print(f"Player {mark} won!")
            break
        if is_draw(board):
            print_board(board)
            print("It's a draw!")
            break
        current = (current + 1) % PLAYER_COUNT

if __name__ == '__main__':
    main()
