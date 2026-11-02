import os
import random

ROWS = 6
COLS = 7
PLAYERS = 2
WIN_COUNT = 4
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
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    print("  " + "   ".join(letters[:COLS]))
    print("+---"*COLS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---"*COLS + "+")

def is_valid_column(col_letter):
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if col_letter in letters[:COLS]:
        return True
    return False

def column_to_index(col_letter):
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    return letters.index(col_letter)

def place_checker(board, col, checker):
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return True
    return False # column full

def check_line(line, checker):
    count = 0
    for c in line:
        if c == checker:
            count += 1
            if count == WIN_COUNT:
                return True
        else:
            count = 0
    return False

def check_win(board, checker):
    # horizontal
    for r in range(ROWS):
        for c in range(COLS - WIN_COUNT +1):
            line = board[r][c:c+WIN_COUNT]
            if all(x == checker for x in line):
                return True
    # vertical
    for c in range(COLS):
        for r in range(ROWS - WIN_COUNT +1):
            line = [board[r+i][c] for i in range(WIN_COUNT)]
            if all(x == checker for x in line):
                return True
    # diagonal down-right
    for r in range(ROWS - WIN_COUNT +1):
        for c in range(COLS - WIN_COUNT +1):
            line = [board[r+i][c+i] for i in range(WIN_COUNT)]
            if all(x == checker for x in line):
                return True
    # diagonal up-right
    for r in range(WIN_COUNT-1, ROWS):
        for c in range(COLS - WIN_COUNT +1):
            line = [board[r - i][c + i] for i in range(WIN_COUNT)]
            if all(x == checker for x in line):
                return True
    return False

def check_draw(board):
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == " ":
                return False
    return True

def get_player_input(current_checker):
    while True:
        move = input("Player " + current_checker + ", please enter a column: ")
        move = move.strip().upper()
        if len(move) != 1:
            continue
        if not is_valid_column(move):
            continue
        return move

def main():
    board = create_board()
    players = CHECKERS[:PLAYERS]
    current_i = random.randint(0, PLAYERS-1)
    print_board(board)
    while True:
        checker = players[current_i]
        move = get_player_input(checker)
        col = column_to_index(move)
        can_place = place_checker(board, col, checker)
        if not can_place:
            # lose turn
            current_i = (current_i+1) % PLAYERS
            print_board(board)
            continue
        print_board(board)
        if check_win(board, checker):
            print("Player " + checker + " won!")
            break
        if check_draw(board):
            print("Game is a draw!")
            break
        current_i = (current_i +1) % PLAYERS

if __name__ == "__main__":
    main()
