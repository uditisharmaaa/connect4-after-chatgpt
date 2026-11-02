import os
import random

ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']  # max 5 players
WIN_COUNT = 4

def clear():
    os.system('clear')

def create_board():
    board = []
    for _ in range(ROWS):
        row = []
        for _ in range(COLS):
            row.append(' ')
        board.append(row)
    return board

def print_board(board):
    clear()
    letters = [chr(ord('A')+i) for i in range(COLS)]
    print("  " + "   ".join(letters))
    print("+---"*COLS + "+")
    for r in range(ROWS):
        print("| " + " | ".join(board[r]) + " |")
        print("+---"*COLS + "+")

def get_column_index(letter):
    if len(letter) != 1:
        return -1
    c = ord(letter) - ord('A')
    if 0 <= c < COLS:
        return c
    return -1

def is_valid_move(board, col):
    if col < 0 or col >= COLS:
        return False
    if board[0][col] != ' ':
        return False
    return True

def place_checker(board, col, checker):
    for row in range(ROWS-1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = checker
            return row
    return -1

def check_win(board, row, col, checker):
    # horizontal
    count = 0
    for c in range(COLS):
        if board[row][c] == checker:
            count += 1
            if count == WIN_COUNT:
                return True
        else:
            count = 0

    # vertical
    count = 0
    for r in range(ROWS):
        if board[r][col] == checker:
            count += 1
            if count == WIN_COUNT:
                return True
        else:
            count = 0

    # diagonal \
    count = 0
    start_r = row
    start_c = col
    while start_r > 0 and start_c > 0:
        start_r -= 1
        start_c -= 1
    while start_r < ROWS and start_c < COLS:
        if board[start_r][start_c] == checker:
            count += 1
            if count == WIN_COUNT:
                return True
        else:
            count = 0
        start_r += 1
        start_c += 1

    # diagonal /
    count = 0
    start_r = row
    start_c = col
    while start_r < ROWS-1 and start_c > 0:
        start_r += 1
        start_c -= 1
    while start_r >= 0 and start_c < COLS:
        if board[start_r][start_c] == checker:
            count += 1
            if count == WIN_COUNT:
                return True
        else:
            count = 0
        start_r -= 1
        start_c += 1

    return False

def is_draw(board):
    for c in range(COLS):
        if board[0][c] == ' ':
            return False
    return True

def main():
    board = create_board()
    players = CHECKERS[:PLAYERS]
    current_player = random.randint(0, PLAYERS-1)
    print_board(board)
    while True:
        player_checker = players[current_player]
        print(f"Player {player_checker}, please enter a column:")

        valid_input = False
        while not valid_input:
            move = input().strip().upper()
            col = get_column_index(move)
            if col == -1:
                print("Invalid input. Please enter a valid column letter:")
                continue
            if not is_valid_move(board, col):
                # losing turn if column full
                print("Column full. You lose your turn.")
                valid_input = True
                row = -1
            else:
                row = place_checker(board, col, player_checker)
                valid_input = True

        print_board(board)

        if row != -1:
            if check_win(board, row, col, player_checker):
                print(f"Player {player_checker} won!")
                break
            if is_draw(board):
                print("The game is a draw.")
                break

        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
