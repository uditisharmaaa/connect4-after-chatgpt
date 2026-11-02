import random
import os

ROWS = 6
COLS = 7
NUM_PLAYERS = 2
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
        print("+" + "---+" * COLS)
        line = "|"
        for c in range(COLS):
            line += " " + board[r][c] + " |"
        print(line)
    print("+" + "---+" * COLS)

def get_player_input(player, board):
    while True:
        col = input(f"Player {player}, please enter a column: ")
        if len(col) != 1:
            continue
        col = col.upper()
        if not ('A' <= col <= chr(ord('A') + COLS - 1)):
            continue
        col_index = ord(col) - ord('A')
        if board[0][col_index] != " ":
            # Column full, lose turn
            print("Column is full, you lose your turn.")
            return -1
        return col_index

def place_checker(board, col, checker):
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return r, col
    return -1, -1

def check_win(board, r, c, checker):
    # horizontal
    count = 0
    for col in range(COLS):
        if board[r][col] == checker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
    # vertical
    count = 0
    for row in range(ROWS):
        if board[row][c] == checker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
    # diagonal \
    count = 0
    start_row = r
    start_col = c
    while start_row > 0 and start_col > 0:
        start_row -= 1
        start_col -= 1
    while start_row < ROWS and start_col < COLS:
        if board[start_row][start_col] == checker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
        start_row += 1
        start_col += 1
    # diagonal /
    count = 0
    start_row = r
    start_col = c
    while start_row < ROWS -1 and start_col > 0:
        start_row +=1
        start_col -=1
    while start_row >=0 and start_col < COLS:
        if board[start_row][start_col] == checker:
            count +=1
            if count ==4:
                return True
        else:
            count = 0
        start_row -=1
        start_col +=1
    return False

def check_draw(board):
    for c in range(COLS):
        if board[0][c] == " ":
            return False
    return True

def main():
    board = create_board()
    players = CHECKERS[:NUM_PLAYERS]
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    print_board(board)

    while True:
        player = players[current_player_index]
        col = get_player_input(player, board)
        if col == -1:
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            print_board(board)
            continue
        r, c = place_checker(board, col, player)
        print_board(board)
        if check_win(board, r, c, player):
            print(f"Player {player} won!")
            break
        if check_draw(board):
            print("The game is a draw!")
            break
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
