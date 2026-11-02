import os, random

ROWS, COLS = 6, 7
PLAYERS = ['X', 'O', 'V', 'H', 'M']  # max 5 players
PLAYER_COUNT = 3  # change between 2-5
PLAYERS = PLAYERS[:PLAYER_COUNT]

def clear(): os.system('clear')

def create_board():
    return [[' ']*COLS for _ in range(ROWS)]

def print_board(board):
    clear()
    print(' ' + ' '.join('ABCDEFG'))
    for row in board:
        print('|' + '|'.join(row) + '|')
    print('-' * (2*COLS+1))

def valid_col(col):
    return col in 'ABCDEFG'

def get_col_idx(c):
    return ord(c) - ord('A')

def drop_piece(board, col, piece):
    for r in reversed(range(ROWS)):
        if board[r][col] == ' ':
            board[r][col] = piece
            return r
    return -1

def check_win(board, r, c, piece):
    directions = [(1,0), (0,1), (1,1), (1,-1)]
    for dr, dc in directions:
        count = 1
        for d in [1,-1]:
            nr, nc = r, c
            while True:
                nr += dr*d
                nc += dc*d
                if 0 <= nr < ROWS and 0 <= nc < COLS and board[nr][nc] == piece:
                    count += 1
                else: break
        if count >= 4: return True
    return False

def board_full(board):
    return all(board[0][c] != ' ' for c in range(COLS))

def main():
    board = create_board()
    current_player = random.choice(range(PLAYER_COUNT))

    while True:
        print_board(board)
        p = PLAYERS[current_player]
        move = input(f"Player {p}, pick column A-{chr(ord('A')+COLS-1)}: ").upper()
        if not (len(move) == 1 and valid_col(move)):
            print("Invalid column. Try again.")
            continue

        col = get_col_idx(move)
        row = drop_piece(board, col, p)
        if row == -1:
            print("Column full. Try again.")
            continue

        if check_win(board, row, col, p):
            print_board(board)
            print(f"Player {p} wins!")
            break
        if board_full(board):
            print_board(board)
            print("It's a draw!")
            break
        
        current_player = (current_player + 1) % PLAYER_COUNT

if __name__ == '__main__':
    main()
