import os, random

ROWS, COLS = 6, 7
PLAYERS = ['X', 'O', 'V', 'H', 'M']  # Allowed players
N_PLAYERS = 3  # Set number of players here (2 to 5)
PLAYERS = PLAYERS[:N_PLAYERS]
COLUMNS = "ABCDEFG"

def clear(): os.system('clear')

def print_board(board):
    print(" "+ " ".join(COLUMNS))
    for row in board:
        print("|" + "|".join(row) + "|")
    print("+" + "-+"*COLS)

def check_win(board, r, c, p):
    directions = [(0,1),(1,0),(1,1),(1,-1)]
    for dr, dc in directions:
        count = 1
        for d in [1,-1]:
            nr, nc = r + d*dr, c + d*dc
            while 0 <= nr < ROWS and 0 <= nc < COLS and board[nr][nc] == p:
                count += 1
                nr += d*dr
                nc += d*dc
        if count >= 4:
            return True
    return False

def is_draw(board):
    return all(board[0][c] != ' ' for c in range(COLS))

def drop_piece(board, col, player):
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == ' ':
            board[r][col] = player
            return r, col
    return -1, -1

def main():
    board = [[' ']*COLS for _ in range(ROWS)]
    current = random.randint(0, N_PLAYERS-1)

    while True:
        clear()
        print_board(board)
        player = PLAYERS[current]
        move = input(f"Player {player}, choose column (A-{COLUMNS[N_PLAYERS-1]}): ").upper()
        if move not in COLUMNS[:COLS]:
            continue
        col = COLUMNS.index(move)
        if board[0][col] != ' ':
            continue
        r, c = drop_piece(board, col, player)
        if check_win(board, r, c, player):
            clear()
            print_board(board)
            print(f"Player {player} wins!")
            break
        if is_draw(board):
            clear()
            print_board(board)
            print("It's a draw!")
            break
        current = (current + 1) % N_PLAYERS

if __name__ == "__main__":
    main()
