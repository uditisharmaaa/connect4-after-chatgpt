import os, random

ROWS, COLS = 6, 7
PLAYERS = 2
CHECKERS = "XOVHM"

def clear():
    os.system('clear')

def create_board():
    return [[" "]*COLS for _ in range(ROWS)]

def print_board(board):
    clear()
    print("  " + "   ".join(chr(ord('A')+i) for i in range(COLS)))
    print("+---"*COLS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---"*COLS + "+")

def input_column(board, player):
    valid_cols = [chr(ord('A')+i) for i in range(COLS)]
    while True:
        col = input(f"Player {player}, please enter a column: ").strip().upper()
        if col not in valid_cols:
            continue
        c = ord(col) - ord('A')
        if board[0][c] != " ":
            # column full, lose turn
            return None
        return c

def place_checker(board, col, checker):
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return r, col

def check_win(board, r, c, checker):
    directions = [(0,1),(1,0),(1,1),(1,-1)]
    for dr, dc in directions:
        count = 1
        for s in [1,-1]:
            nr, nc = r, c
            while True:
                nr += dr*s
                nc += dc*s
                if 0 <= nr < ROWS and 0 <= nc < COLS and board[nr][nc]==checker:
                    count +=1
                else:
                    break
        if count >=4:
            return True
    return False

def board_full(board):
    return all(cell != " " for cell in board[0])

def main():
    board = create_board()
    players = CHECKERS[:PLAYERS]
    turn = random.randint(0, PLAYERS-1)
    print_board(board)
    while True:
        player = players[turn]
        col = input_column(board, player)
        if col is None:
            turn = (turn +1)%PLAYERS
            continue
        r, c = place_checker(board, col, player)
        print_board(board)
        if check_win(board, r, c, player):
            print(f"Player {player} won!")
            break
        if board_full(board):
            print("Game is a draw!")
            break
        turn = (turn +1)%PLAYERS

if __name__ == "__main__":
    main()
