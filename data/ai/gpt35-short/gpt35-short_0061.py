import os, random

ROWS, COLS = 6, 7
PLAYERS = ['X', 'O', 'V', 'H', 'M']
COL_LABELS = 'ABCDEFG'

def clear(): os.system('clear')

def create_board():
    return [['.' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    clear()
    print(' '.join(COL_LABELS))
    for row in board:
        print(' '.join(row))
    print()

def get_move(player, board):
    while True:
        move = input(f"Player {player}, choose column (A-G): ").upper()
        if move in COL_LABELS:
            c = COL_LABELS.index(move)
            if board[0][c] == '.':
                return c
            else:
                print("Column full!")
        else:
            print("Invalid input!")

def make_move(board, col, player):
    for r in reversed(range(ROWS)):
        if board[r][col] == '.':
            board[r][col] = player
            return r, col

def check_win(board, r, c, player):
    directions = [(0,1),(1,0),(1,1),(1,-1)]
    for dr, dc in directions:
        count = 1
        for d in (1, -1):
            nr, nc = r, c
            while True:
                nr += dr*d
                nc += dc*d
                if 0 <= nr < ROWS and 0 <= nc < COLS and board[nr][nc] == player:
                    count += 1
                else:
                    break
        if count >= 4:
            return True
    return False

def full_board(board):
    return all(board[0][c] != '.' for c in range(COLS))

def main():
    n = 0
    while not (2 <= n <= 5):
        try:
            n = int(input("Number of players (2-5): "))
        except: pass

    players = PLAYERS[:n]
    board = create_board()
    turn = random.randint(0, n-1)

    while True:
        print_board(board)
        col = get_move(players[turn], board)
        r, c = make_move(board, col, players[turn])

        if check_win(board, r, c, players[turn]):
            print_board(board)
            print(f"Player {players[turn]} wins!")
            break
        if full_board(board):
            print_board(board)
            print("It's a draw!")
            break

        turn = (turn + 1) % n

if __name__=="__main__":
    main()
