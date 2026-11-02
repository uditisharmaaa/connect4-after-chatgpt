import os, random

ROWS, COLS = 6, 7
PLAYERS = ['X', 'O', 'V', 'H', 'M']  # up to 5 players
COLUMNS = "ABCDEFG"

def clear(): os.system('clear')

def create_board():
    return [[' ']*COLS for _ in range(ROWS)]

def print_board(b):
    print(' ' + ' '.join(COLUMNS))
    for row in b:
        print('|' + '|'.join(row) + '|')
    print('-'*(2*COLS+1))

def col_to_index(c):
    return COLUMNS.find(c.upper())

def valid_move(b, col):
    return 0 <= col < COLS and b[0][col] == ' '

def make_move(b, col, p):
    for r in reversed(range(ROWS)):
        if b[r][col] == ' ':
            b[r][col] = p
            return r, col

def check_dir(b, r, c, dr, dc, p):
    count = 0
    for _ in range(4):
        if 0 <= r < ROWS and 0 <= c < COLS and b[r][c] == p:
            count += 1
            r += dr
            c += dc
        else:
            break
    return count == 4

def win(b, r, c, p):
    return any(check_dir(b, r, c, dr, dc, p)
               for dr, dc in [(0,1),(1,0),(1,1),(1,-1)])

def draw(b):
    return all(b[0][c] != ' ' for c in range(COLS))

def main():
    p_count = 0
    while not (2 <= p_count <= 5):
        try:
            p_count = int(input(f"Players (2-5), use first {PLAYERS[:p_count]}: "))
        except:
            pass
    players = PLAYERS[:p_count]
    board = create_board()
    current = random.choice(players)

    while True:
        clear()
        print_board(board)
        print(f"Player {current}'s turn.")
        move = input("Choose a column (A-G): ").strip().upper()
        col = col_to_index(move)
        if col == -1 or not valid_move(board, col):
            print("Invalid move. Try again.")
            continue

        r, c = make_move(board, col, current)
        if win(board, r, c, current):
            clear()
            print_board(board)
            print(f"Player {current} wins!")
            break
        if draw(board):
            clear()
            print_board(board)
            print("It's a draw!")
            break

        current = players[(players.index(current) + 1) % p_count]

if __name__ == "__main__":
    main()
