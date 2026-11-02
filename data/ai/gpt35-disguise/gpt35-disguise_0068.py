import os
import random

ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def clear_screen():
    os.system('clear')

def create_board():
    board = []
    for r in range(ROWS):
        row = []
        for c in range(COLS):
            row.append(" ")
        board.append(row)
    return board

def print_board(board):
    clear_screen()
    # print column letters
    letters = ""
    for i in range(COLS):
        letters += "  " + chr(ord('A') + i) + " "
    print(letters)
    
    # print rows
    for r in range(ROWS):
        line = "+"
        for c in range(COLS):
            line += "---+"
        print(line)
        rowline = "|"
        for c in range(COLS):
            rowline += " " + board[r][c] + " |"
        print(rowline)
    print(line)

def valid_col_input(col):
    if len(col) != 1:
        return False
    c = col.upper()
    if c < 'A' or c >= chr(ord('A') + COLS):
        return False
    return True

def column_full(board, col):
    return board[0][col] != " "

def put_checker(board, col, checker):
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return r, col
    return -1, -1  # if full

def check_line(board, r, c, dr, dc, checker):
    count = 0
    for i in range(4):
        rr = r + dr*i
        cc = c + dc*i
        if rr < 0 or rr >= ROWS or cc < 0 or cc >= COLS:
            return False
        if board[rr][cc] != checker:
            return False
    return True

def check_win(board, checker):
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == checker:
                # check horizontal right
                if check_line(board, r, c, 0, 1, checker):
                    return True
                # check vertical down
                if check_line(board, r, c, 1, 0, checker):
                    return True
                # check diagonal down-right
                if check_line(board, r, c, 1, 1, checker):
                    return True
                # check diagonal down-left
                if check_line(board, r, c, 1, -1, checker):
                    return True
    return False

def board_full(board):
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
        print("Player {}, please enter a column:".format(players[current]))
        inp = input()
        while not valid_col_input(inp):
            print("Invalid input. Player {}, please enter a column:".format(players[current]))
            inp = input()
        col = ord(inp.upper()) - ord('A')
        
        if column_full(board, col):
            # turn lost if full column
            current = (current + 1) % PLAYERS
            print_board(board)
            continue
        
        put_checker(board, col, players[current])
        print_board(board)
        
        if check_win(board, players[current]):
            print("Player {} won!".format(players[current]))
            break
        if board_full(board):
            print("Game is a draw!")
            break
        
        current = (current + 1) % PLAYERS

if __name__ == "__main__":
    main()
