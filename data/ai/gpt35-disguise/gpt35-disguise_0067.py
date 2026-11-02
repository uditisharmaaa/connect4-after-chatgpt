import os
import random

ROWS = 6
COLS = 7
WIN_COUNT = 4
PLAYER_COUNT = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

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
    letters = [chr(ord('A') + i) for i in range(COLS)]
    print("  " + "   ".join(letters))
    for r in range(ROWS):
        print("+" + "---+"*COLS)
        line = "|"
        for c in range(COLS):
            line += " " + board[r][c] + " |"
        print(line)
    print("+" + "---+"*COLS)

def get_column_index(col_letter):
    if len(col_letter) != 1:
        return -1
    col = ord(col_letter) - ord('A')
    if 0 <= col < COLS:
        return col
    else:
        return -1

def is_column_full(board, col):
    return board[0][col] != " "

def place_checker(board, col, checker):
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return True
    return False

def check_horizontal(board, checker):
    for r in range(ROWS):
        count = 0
        for c in range(COLS):
            if board[r][c] == checker:
                count +=1
                if count == WIN_COUNT:
                    return True
            else:
                count = 0
    return False

def check_vertical(board, checker):
    for c in range(COLS):
        count = 0
        for r in range(ROWS):
            if board[r][c] == checker:
                count +=1
                if count == WIN_COUNT:
                    return True
            else:
                count = 0
    return False

def check_diagonal(board, checker):
    # descending diagonal (\)
    for r in range(ROWS - WIN_COUNT +1):
        for c in range(COLS - WIN_COUNT +1):
            win = True
            for i in range(WIN_COUNT):
                if board[r+i][c+i] != checker:
                    win = False
                    break
            if win:
                return True
    # ascending diagonal (/)
    for r in range(WIN_COUNT -1, ROWS):
        for c in range(COLS - WIN_COUNT +1):
            win = True
            for i in range(WIN_COUNT):
                if board[r - i][c + i] != checker:
                    win = False
                    break
            if win:
                return True
    return False

def check_win(board, checker):
    return check_horizontal(board, checker) or check_vertical(board, checker) or check_diagonal(board, checker)

def check_draw(board):
    for c in range(COLS):
        if board[0][c] == " ":
            return False
    return True

def main():
    board = create_board()
    players = CHECKERS[:PLAYER_COUNT]
    current_player = random.choice(range(PLAYER_COUNT))
    while True:
        clear_screen()
        print_board(board)
        print("Player " + players[current_player] + ", please enter a column:")
        col_input = input().strip().upper()
        col = get_column_index(col_input)
        if col == -1:
            continue
        if is_column_full(board, col):
            # player loses turn
            current_player = (current_player + 1) % PLAYER_COUNT
            continue
        placed = place_checker(board, col, players[current_player])
        if not placed:
            # should not happen because of is_column_full check
            current_player = (current_player +1) % PLAYER_COUNT
            continue
        if check_win(board, players[current_player]):
            clear_screen()
            print_board(board)
            print("Player " + players[current_player] + " won!")
            break
        if check_draw(board):
            clear_screen()
            print_board(board)
            print("Game is a draw!")
            break
        current_player = (current_player +1) % PLAYER_COUNT

if __name__ == "__main__":
    main()
