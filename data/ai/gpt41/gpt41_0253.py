import os
import random
import string

# --- CONSTANTS ---
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M'][:PLAYERS]
WIN_LENGTH = 4
MAX_COLS = 26

# --- BOARD SETUP ---
def create_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    os.system('clear')
    # Column labels
    col_labels = [chr(ord('A') + i) for i in range(len(board[0]))]
    print('  ', '   '.join(col_labels))
    print('+' + '---+'*len(board[0]))
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+' + '---+'*len(board[0]))

# --- INPUT/OUTPUT HELPERS ---
def get_valid_column(board, taken_turn):
    cols = len(board[0])
    valid_cols = [chr(ord('A') + i) for i in range(cols)]
    while True:
        move = input("Please enter a column: ").strip().upper()
        if len(move) != 1 or move not in valid_cols:
            print("Invalid column. Try again.")
            continue
        idx = valid_cols.index(move)
        if board[0][idx] != ' ':
            print("Column full. You lose your turn." if taken_turn else "Column full. Try again.")
            if taken_turn:
                return None
            continue
        return idx

# --- GAME LOGIC ---
def drop_checker(board, col, checker):
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = checker
            return board.index(row), col

def is_winner(board, row, col, checker):
    # Check all directions: horizontal, vertical, both diagonals
    def count(dx, dy):
        count = 0
        r, c = row+dx, col+dy
        while 0 <= r < ROWS and 0 <= c < len(board[0]) and board[r][c] == checker:
            count += 1
            r += dx
            c += dy
        return count

    return (
        1 + count(0,1) + count(0,-1) >= WIN_LENGTH or # horizontal
        1 + count(1,0) + count(-1,0) >= WIN_LENGTH or # vertical
        1 + count(1,1) + count(-1,-1) >= WIN_LENGTH or # diagonal \
        1 + count(1,-1) + count(-1,1) >= WIN_LENGTH    # diagonal /
    )

def is_draw(board):
    return all(cell != ' ' for cell in board[0])

def main():
    board = create_board(ROWS, COLS)
    players = CHECKERS
    current_player = random.randint(0, PLAYERS-1)
    print_board(board)
    print(f"Player {players[current_player]} starts!\n")
    game_over = False

    while not game_over:
        print_board(board)
        print(f"Player {players[current_player]}, ", end='')
        col = get_valid_column(board, True)
        if col is None:
            # Lose turn if column is full
            current_player = (current_player + 1) % PLAYERS
            continue
        row, col = drop_checker(board, col, players[current_player])
        if is_winner(board, row, col, players[current_player]):
            print_board(board)
            print(f"Player {players[current_player]} won!")
            break
        if is_draw(board):
            print_board(board)
            print("It's a draw!")
            break
        current_player = (current_player + 1) % PLAYERS

if __name__ == '__main__':
    main()
