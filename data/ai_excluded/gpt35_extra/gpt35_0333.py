import os
import random

ROWS, COLS = 6, 7
PLAYERS = ["X", "O"]  # for submission: 2 players, max 5 allowed ('X', 'O', 'V', 'H', 'M')

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" "]*cols for _ in range(rows)]

def print_board(board):
    clear_screen()
    header = "  " + "   ".join(chr(ord('A') + i) for i in range(len(board[0])))
    print(header)
    line = "+---"*len(board[0]) + "+"
    for row in board:
        print(line)
        print("| " + " | ".join(row) + " |")
    print(line)

def valid_column(col_char, board):
    if len(col_char) != 1 or not ('A' <= col_char <= chr(ord('A') + len(board[0]) - 1)):
        return False
    col = ord(col_char) - ord('A')
    return board[0][col] == " "

def place_checker(board, col_char, checker):
    col = ord(col_char) - ord('A')
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return r, col
    return None

def check_winner(board, r, c, checker):
    directions = [(0,1),(1,0),(1,1),(1,-1)]
    for dr, dc in directions:
        count = 1
        for d in [1,-1]:
            rr, cc = r, c
            while True:
                rr += dr*d
                cc += dc*d
                if 0 <= rr < ROWS and 0 <= cc < COLS and board[rr][cc] == checker:
                    count += 1
                else:
                    break
        if count >= 4:
            return True
    return False

def board_full(board):
    return all(cell != " " for cell in board[0])

def main():
    board = create_board(ROWS, COLS)
    players = PLAYERS[:2] # for submission
    current = random.randint(0, len(players)-1)
    print_board(board)
    while True:
        checker = players[current]
        move = input(f"Player {checker}, please enter a column: ").strip().upper()
        if not valid_column(move, board):
            print("Invalid move, try again.")
            continue
        pos = place_checker(board, move, checker)
        if pos is None:  # column full, lose turn
            print("Column full, turn lost.")
        else:
            print_board(board)
            if check_winner(board, *pos, checker):
                print(f"Player {checker} won!")
                break
            if board_full(board):
                print("Game is a draw!")
                break
        current = (current + 1) % len(players)

if __name__ == "__main__":
    main()
