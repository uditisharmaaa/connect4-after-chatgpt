import os
import random

ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
player_checkers = CHECKERS[:PLAYERS]

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    os.system('clear')
    print("  " + "   ".join([chr(i) for i in range(65, 65 + len(board[0]))]))
    print("+" + "---+" * len(board[0]))
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * len(board[0]))

def get_move(board):
    while True:
        col = input("Please enter a column: ").upper()
        if len(col) != 1 or col < "A" or col >= chr(65 + len(board[0])):
            print("Invalid column. Try again.")
            continue
        col = ord(col) - 65
        if board[0][col] != " ":
            print("Column full. Choose another.")
            continue
        return col

def place_checker(board, col, checker):
    for row in reversed(board):
        if row[col] == " ":
            row[col] = checker
            break

def check_win(board, checker):
    def check_line(x, y, dx, dy):
        for _ in range(4):
            if board[y][x] != checker:
                return False
            x, y = x + dx, y + dy
        return True

    for y in range(len(board)):
        for x in range(len(board[0])):
            if (
                x <= len(board[0]) - 4 and check_line(x, y, 1, 0) or
                y <= len(board) - 4 and check_line(x, y, 0, 1) or
                x <= len(board[0]) - 4 and y <= len(board) - 4 and check_line(x, y, 1, 1) or
                x >= 3 and y <= len(board) - 4 and check_line(x, y, -1, 1)
            ):
                return True
    return False

def check_draw(board):
    return all(board[0][col] != " " for col in range(len(board[0])))

def connect4():
    board = create_board(ROWS, COLS)
    current_player = random.randint(0, PLAYERS - 1)

    print_board(board)
    while True:
        print(f"Player {player_checkers[current_player]}, your turn")
        col = get_move(board)
        place_checker(board, col, player_checkers[current_player])
        print_board(board)
        
        if check_win(board, player_checkers[current_player]):
            print(f"Player {player_checkers[current_player]} won!")
            break
        if check_draw(board):
            print("It's a draw!")
            break
        
        current_player = (current_player + 1) % PLAYERS

connect4()
