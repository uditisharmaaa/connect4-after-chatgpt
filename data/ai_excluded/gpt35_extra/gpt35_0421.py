import os
import random

ROWS, COLS = 6, 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_LENGTH = 4

def clear():
    os.system('clear')

def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    clear()
    print("  " + "   ".join(chr(ord('A') + i) for i in range(COLS)))
    print("+---" * COLS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLS + "+")

def valid_column(inp, board):
    if len(inp) != 1 or not ('A' <= inp <= chr(ord('A') + COLS -1)):
        return False
    col = ord(inp) - ord('A')
    return board[0][col] == " "

def drop_checker(board, col, checker):
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return r, col
    return -1, -1

def check_direction(board, r, c, dr, dc, checker):
    count = 0
    for i in range(WIN_LENGTH):
        rr, cc = r + dr*i, c + dc*i
        if 0 <= rr < ROWS and 0 <= cc < COLS and board[rr][cc] == checker:
            count += 1
        else:
            break
    return count == WIN_LENGTH

def check_win(board, r, c, checker):
    return (check_direction(board, r, c, 0, 1, checker) or
            check_direction(board, r, c, 1, 0, checker) or
            check_direction(board, r, c, 1, 1, checker) or
            check_direction(board, r, c, 1, -1, checker))

def full_board(board):
    return all(board[0][c] != " " for c in range(COLS))

def main():
    board = create_board()
    players = CHECKERS[:PLAYERS]
    turn = random.randint(0, PLAYERS -1)
    print_board(board)
    while True:
        checker = players[turn]
        inp = input(f"Player {checker}, please enter a column: ").upper()
        if not valid_column(inp, board):
            # If column is full, player loses turn
            col = ord(inp) - ord('A') if len(inp) == 1 and 'A' <= inp <= chr(ord('A') + COLS - 1) else -1
            if 0 <= col < COLS and board[0][col] != " ":
                turn = (turn + 1) % PLAYERS
                print_board(board)
                continue
            else:
                continue
        col = ord(inp) - ord('A')
        r, c = drop_checker(board, col, checker)
        print_board(board)
        if r == -1:
            # Column full, lost turn
            turn = (turn +1) % PLAYERS
            continue
        if check_win(board, r, c, checker):
            print(f"Player {checker} won!")
            break
        if full_board(board):
            print("It is a draw!")
            break
        turn = (turn +1) % PLAYERS

if __name__ == "__main__":
    main()
