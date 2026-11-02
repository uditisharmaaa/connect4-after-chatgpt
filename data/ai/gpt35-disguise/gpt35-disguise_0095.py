import os
import random

ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board():
    board = []
    for _ in range(ROWS):
        row = [" "]*COLS
        board.append(row)
    return board

def print_board(board):
    os.system('clear')
    letters = [chr(ord('A')+i) for i in range(COLS)]
    print("  " + "   ".join(letters))
    line = "+---"*COLS + "+"
    for r in range(ROWS):
        print(line)
        row_str = "|"
        for c in range(COLS):
            row_str += " " + board[r][c] + " |"
        print(row_str)
    print(line)

def get_move(player, board):
    while True:
        col = input(f"Player {player}, please enter a column: ")
        if len(col) != 1:
            continue
        if not col.isalpha():
            continue
        col = col.upper()
        idx = ord(col) - ord('A')
        if idx < 0 or idx >= COLS:
            continue
        if board[0][idx] != " ":
            # Column full, player loses turn according to assignment
            return -1
        return idx

def place_checker(board, col, checker):
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return r, col
    return -1, -1

def check_win(board, checker):
    # horizontal
    for r in range(ROWS):
        count = 0
        for c in range(COLS):
            if board[r][c] == checker:
                count +=1
                if count == 4:
                    return True
            else:
                count = 0
    # vertical
    for c in range(COLS):
        count = 0
        for r in range(ROWS):
            if board[r][c] == checker:
                count +=1
                if count == 4:
                    return True
            else:
                count = 0
    # diagonal down-right
    for r in range(ROWS-3):
        for c in range(COLS-3):
            if board[r][c] == checker and board[r+1][c+1] == checker and board[r+2][c+2] == checker and board[r+3][c+3] == checker:
                return True
    # diagonal up-right
    for r in range(3, ROWS):
        for c in range(COLS-3):
            if board[r][c] == checker and board[r-1][c+1] == checker and board[r-2][c+2] == checker and board[r-3][c+3] == checker:
                return True
    return False

def check_draw(board):
    for c in range(COLS):
        if board[0][c] == " ":
            return False
    return True

def main():
    board = create_board()
    players = CHECKERS[:PLAYERS]
    current = random.randint(0, PLAYERS-1)
    print_board(board)

    while True:
        player = players[current]
        col = get_move(player, board)
        if col == -1:
            current = (current +1) % PLAYERS
            continue
        r, c = place_checker(board, col, player)
        print_board(board)

        if check_win(board, player):
            print(f"Player {player} won!")
            break
        if check_draw(board):
            print("Game is a draw!")
            break
        current = (current +1) % PLAYERS

if __name__ == "__main__":
    main()
