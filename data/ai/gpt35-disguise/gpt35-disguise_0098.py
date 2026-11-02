import os
import random

ROWS = 6
COLS = 7
PLAYERS = 2
WIN_COUNT = 4

CHECKERS = ["X", "O", "V", "H", "M"]

def clear():
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
    clear()
    # print column letters
    letters = [chr(ord('A') + i) for i in range(COLS)]
    print("  " + "   ".join(letters))
    # print rows with separators
    for r in range(ROWS):
        print("+---"*COLS + "+")
        row_str = "|"
        for c in range(COLS):
            row_str += " " + board[r][c] + " |"
        print(row_str)
    print("+---"*COLS + "+")

def is_valid_col(col_letter):
    if len(col_letter) != 1:
        return False
    if col_letter < 'A' or col_letter >= chr(ord('A') + COLS):
        return False
    return True

def get_col_index(col_letter):
    return ord(col_letter) - ord('A')

def place_checker(board, col, checker):
    # start from bottom row up and place checker on first empty
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return True
    return False  # column full

def check_win(board, checker):
    # Horizontal check
    for r in range(ROWS):
        for c in range(COLS - WIN_COUNT +1):
            win = True
            for i in range(WIN_COUNT):
                if board[r][c+i] != checker:
                    win = False
                    break
            if win:
                return True

    # Vertical check
    for c in range(COLS):
        for r in range(ROWS - WIN_COUNT +1):
            win = True
            for i in range(WIN_COUNT):
                if board[r+i][c] != checker:
                    win = False
                    break
            if win:
                return True

    # Diagonal down-right \
    for r in range(ROWS - WIN_COUNT +1):
        for c in range(COLS - WIN_COUNT +1):
            win = True
            for i in range(WIN_COUNT):
                if board[r+i][c+i] != checker:
                    win = False
                    break
            if win:
                return True

    # Diagonal up-right /
    for r in range(WIN_COUNT-1, ROWS):
        for c in range(COLS - WIN_COUNT +1):
            win = True
            for i in range(WIN_COUNT):
                if board[r-i][c+i] != checker:
                    win = False
                    break
            if win:
                return True

    return False

def is_draw(board):
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == " ":
                return False
    return True

def main():
    board = create_board()
    players = CHECKERS[:PLAYERS]
    current_player_index = random.randint(0, PLAYERS-1)
    print_board(board)

    while True:
        player = players[current_player_index]
        valid_input = False
        col_index = -1
        while not valid_input:
            inp = input("Player " + player + ", please enter a column: ").strip().upper()
            if not is_valid_col(inp):
                continue
            col_index = get_col_index(inp)
            if col_index < 0 or col_index >= COLS:
                continue
            # check if column full
            if board[0][col_index] != " ":
                # full column, player loses turn
                valid_input = True
                col_index = -1
                break
            valid_input = True

        if col_index != -1:
            placed = place_checker(board, col_index, player)
            if not placed:
                # column full, lose turn
                pass
        print_board(board)

        if col_index != -1:
            if check_win(board, player):
                print("Player " + player + " won!")
                break

        if is_draw(board):
            print("Draw!")
            break

        # next player
        current_player_index = (current_player_index + 1) % PLAYERS

if __name__ == "__main__":
    main()
