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
    for _ in range(ROWS):
        row = []
        for _ in range(COLS):
            row.append(" ")
        board.append(row)
    return board

def print_board(board):
    clear_screen()
    header = "  "
    for i in range(COLS):
        header += chr(ord('A') + i) + "   "
    print(header)
    for r in range(ROWS):
        line = "+"
        for c in range(COLS):
            line += "---+"
        print(line)
        line = "|"
        for c in range(COLS):
            line += " " + board[r][c] + " |"
        print(line)
    line = "+"
    for c in range(COLS):
        line += "---+"
    print(line)

def is_valid_column(col_char):
    if len(col_char) != 1:
        return False
    if col_char < 'A' or col_char >= chr(ord('A') + COLS):
        return False
    return True

def get_column_index(col_char):
    return ord(col_char) - ord('A')

def place_checker(board, col_idx, checker):
    for row in range(ROWS-1, -1, -1):
        if board[row][col_idx] == " ":
            board[row][col_idx] = checker
            return True
    return False

def check_winner(board, checker):
    # horizontal check
    for r in range(ROWS):
        for c in range(COLS - 3):
            if board[r][c] == checker and board[r][c+1] == checker and board[r][c+2] == checker and board[r][c+3] == checker:
                return True
    # vertical check
    for r in range(ROWS - 3):
        for c in range(COLS):
            if board[r][c] == checker and board[r+1][c] == checker and board[r+2][c] == checker and board[r+3][c] == checker:
                return True
    # diagonal down-right check
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if board[r][c] == checker and board[r+1][c+1] == checker and board[r+2][c+2] == checker and board[r+3][c+3] == checker:
                return True
    # diagonal up-right check
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if board[r][c] == checker and board[r-1][c+1] == checker and board[r-2][c+2] == checker and board[r-3][c+3] == checker:
                return True
    return False

def is_board_full(board):
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == " ":
                return False
    return True

def main():
    board = create_board()
    players = CHECKERS[:PLAYERS]

    current_player = random.randint(0, PLAYERS -1)

    while True:
        print_board(board)
        print("Player {}, please enter a column:".format(players[current_player]))
        inp = input().strip().upper()
        if not is_valid_column(inp):
            print("Invalid column. Try again.")
            continue
        col = get_column_index(inp)
        placed = place_checker(board, col, players[current_player])
        if not placed:
            print("Column full. You lose your turn.")
            current_player = (current_player + 1) % PLAYERS
            continue
        if check_winner(board, players[current_player]):
            print_board(board)
            print("Player {} won!".format(players[current_player]))
            break
        if is_board_full(board):
            print_board(board)
            print("Game is a draw!")
            break
        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
