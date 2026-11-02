import os
import random

ROWS = 6
COLS = 7
NUM_PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def clear():
    os.system('clear')

def create_board():
    board = []
    for _ in range(ROWS):
        row = [' ']*COLS
        board.append(row)
    return board

def print_board(board):
    clear()
    letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    print("  " + "   ".join(letters[:COLS]))
    print("+---"*COLS + "+")
    for r in range(ROWS):
        print("| " + " | ".join(board[r]) + " |")
        print("+---"*COLS + "+")

def check_input(s):
    letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    if len(s) != 1:
        return False
    if s not in letters[:COLS]:
        return False
    return True

def find_row(board, col):
    for r in reversed(range(ROWS)):
        if board[r][col] == ' ':
            return r
    return -1

def place_checker(board, col, checker):
    r = find_row(board, col)
    if r == -1:
        return False
    board[r][col] = checker
    return True

def check_win(board, checker):
    # horizontal
    for r in range(ROWS):
        for c in range(COLS-3):
            if board[r][c] == checker and board[r][c+1] == checker and board[r][c+2] == checker and board[r][c+3] == checker:
                return True
    # vertical
    for c in range(COLS):
        for r in range(ROWS-3):
            if board[r][c] == checker and board[r+1][c] == checker and board[r+2][c] == checker and board[r+3][c] == checker:
                return True
    # diagonal right down
    for r in range(ROWS-3):
        for c in range(COLS-3):
            if board[r][c] == checker and board[r+1][c+1] == checker and board[r+2][c+2] == checker and board[r+3][c+3] == checker:
                return True
    # diagonal left down
    for r in range(ROWS-3):
        for c in range(3, COLS):
            if board[r][c] == checker and board[r+1][c-1] == checker and board[r+2][c-2] == checker and board[r+3][c-3] == checker:
                return True
    return False

def check_draw(board):
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == ' ':
                return False
    return True

def main():
    board = create_board()
    players = CHECKERS[:NUM_PLAYERS]
    current_player_index = random.randint(0, NUM_PLAYERS-1)

    print_board(board)

    while True:
        player = players[current_player_index]
        col_letter = ''
        while True:
            col_letter = input(f"Player {player}, please enter a column: ").upper()
            if not check_input(col_letter):
                continue
            col = ord(col_letter) - ord('A')
            if col < 0 or col >= COLS:
                continue
            row = find_row(board, col)
            if row == -1:
                # column full, lose turn
                break
            else:
                break

        if col_letter == '':
            # somehow no input, continue
            continue

        # if column full, player loses turn
        if row == -1:
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            print_board(board)
            continue

        placed = place_checker(board, col, player)
        print_board(board)

        won = check_win(board, player)
        if won:
            print(f"Player {player} won!")
            break

        if check_draw(board):
            print("The game is a draw.")
            break

        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == '__main__':
    main()
