import os
import random

ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_LENGTH = 4

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
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    print("  ", end="")
    for c in range(COLS):
        print(f" {letters[c]}  ", end="")
    print()
    print("+---"*COLS + "+")
    for r in range(ROWS):
        print("|", end="")
        for c in range(COLS):
            print(f" {board[r][c]} |", end="")
        print()
        print("+---"*COLS + "+")

def get_player_input(player, board):
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    while True:
        move = input(f"Player {CHECKERS[player]}, please enter a column: ")
        if len(move) != 1:
            print("Invalid input. Enter single letter.")
            continue
        move = move.upper()
        if move not in letters[:COLS]:
            print("Invalid column letter.")
            continue
        col = letters.index(move)
        if board[0][col] != " ":
            # column full, lose turn
            print("Column full. You lose your turn.")
            return -1
        return col

def place_checker(board, col, checker):
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return r, col

def check_winner(board, checker):
    # horizontal
    for r in range(ROWS):
        for c in range(COLS - WIN_LENGTH +1):
            count = 0
            for i in range(WIN_LENGTH):
                if board[r][c+i] == checker:
                    count +=1
            if count == WIN_LENGTH:
                return True
    # vertical
    for c in range(COLS):
        for r in range(ROWS - WIN_LENGTH +1):
            count = 0
            for i in range(WIN_LENGTH):
                if board[r+i][c] == checker:
                    count +=1
            if count == WIN_LENGTH:
                return True
    # diagonal down-right
    for r in range(ROWS - WIN_LENGTH +1):
        for c in range(COLS - WIN_LENGTH +1):
            count = 0
            for i in range(WIN_LENGTH):
                if board[r+i][c+i] == checker:
                    count +=1
            if count == WIN_LENGTH:
                return True
    # diagonal up-right
    for r in range(WIN_LENGTH-1, ROWS):
        for c in range(COLS - WIN_LENGTH +1):
            count = 0
            for i in range(WIN_LENGTH):
                if board[r - i][c + i] == checker:
                    count +=1
            if count == WIN_LENGTH:
                return True
    return False

def check_draw(board):
    for c in range(COLS):
        if board[0][c] == " ":
            return False
    return True

def main():
    board = create_board()
    players = PLAYERS
    checkers = CHECKERS[:players]

    current_player = random.randint(0, players-1)

    print_board(board)
    while True:
        col = get_player_input(current_player, board)
        if col == -1:
            # lose turn
            current_player = (current_player +1) % players
            print_board(board)
            continue
        r, c = place_checker(board, col, checkers[current_player])
        print_board(board)
        if check_winner(board, checkers[current_player]):
            print(f"Player {checkers[current_player]} won!")
            break
        if check_draw(board):
            print("Game is a draw!")
            break
        current_player = (current_player +1) % players

if __name__ == "__main__":
    main()
