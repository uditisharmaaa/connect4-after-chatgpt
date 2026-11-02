import os, random

ROWS, COLS = 6, 7
COL_LABELS = 'ABCDEFG'
PLAYERS = ['X', 'O', 'V', 'H', 'M']  # max 5 players
NUM_PLAYERS = 4  # set 2 to 5 players here
PLAYERS = PLAYERS[:NUM_PLAYERS]

def clear(): os.system('clear')

def create_board():
    return [[' ']*COLS for _ in range(ROWS)]

def print_board(board):
    print('  ' + ' '.join(COL_LABELS))
    for row in board:
        print('|'+ '|'.join(row) + '|')
    print('-'*(COLS*2+1))

def valid_col(col, board):
    return col in range(COLS) and board[0][col] == ' '

def drop_piece(board, col, piece):
    for r in reversed(range(ROWS)):
        if board[r][col] == ' ':
            board[r][col] = piece
            return r, col

def check_win(board, piece):
    # horizontal, vertical, diagonal checks
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] != piece:
                continue
            # horizontal
            if c <= COLS-4 and all(board[r][c+i] == piece for i in range(4)):
                return True
            # vertical
            if r <= ROWS-4 and all(board[r+i][c] == piece for i in range(4)):
                return True
            # diag down-right
            if r <= ROWS-4 and c <= COLS-4 and all(board[r+i][c+i] == piece for i in range(4)):
                return True
            # diag down-left
            if r <= ROWS-4 and c >= 3 and all(board[r+i][c-i] == piece for i in range(4)):
                return True
    return False

def check_draw(board):
    return all(board[0][c] != ' ' for c in range(COLS))

def main():
    board = create_board()
    player_idx = random.randint(0, NUM_PLAYERS-1)

    while True:
        clear()
        print_board(board)
        piece = PLAYERS[player_idx]
        inp = input(f"Player {piece}, choose column (A-G): ").upper()
        if inp not in COL_LABELS:
            print("Invalid column. Try again.")
            continue
        col = COL_LABELS.index(inp)
        if not valid_col(col, board):
            print("Column full or invalid. Try again.")
            continue
        drop_piece(board, col, piece)
        if check_win(board, piece):
            clear()
            print_board(board)
            print(f"Player {piece} wins!")
            break
        if check_draw(board):
            clear()
            print_board(board)
            print("It's a draw!")
            break
        player_idx = (player_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
