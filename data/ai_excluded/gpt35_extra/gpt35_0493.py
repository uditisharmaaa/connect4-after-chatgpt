import os
import random

ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_COUNT = 4

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

def valid_input(s, board):
    if len(s) != 1 or not ('A' <= s <= chr(ord('A')+COLS-1)):
        return False
    col = ord(s) - ord('A')
    return board[0][col] == " "

def place_checker(board, col, checker):
    for row in reversed(range(ROWS)):
        if board[row][col] == " ":
            board[row][col] = checker
            return row, col
    return None, None

def check_win(board, r, c, checker):
    directions = [(0,1),(1,0),(1,1),(1,-1)]
    for dr, dc in directions:
        count = 1
        for d in [1, -1]:
            nr, nc = r + dr*d, c + dc*d
            while 0 <= nr < ROWS and 0 <= nc < COLS and board[nr][nc] == checker:
                count += 1
                nr += dr*d
                nc += dc*d
        if count >= WIN_COUNT:
            return True
    return False

def is_draw(board):
    return all(board[0][c] != " " for c in range(COLS))

def main():
    board = create_board()
    players = CHECKERS[:PLAYERS]
    current = random.randint(0, PLAYERS-1)
    print_board(board)

    while True:
        player = players[current]
        inp = input(f"Player {player}, please enter a column: ").strip().upper()
        if not valid_input(inp, board):
            # invalid input: repeat turn
            continue
        col = ord(inp) - ord('A')
        row, col = place_checker(board, col, player)
        if row is None:
            # column full, lose turn
            current = (current + 1) % PLAYERS
            continue
        print_board(board)
        if check_win(board, row, col, player):
            print(f"Player {player} won!")
            break
        if is_draw(board):
            print("Game is a draw!")
            break
        current = (current + 1) % PLAYERS

if __name__ == "__main__":
    main()
