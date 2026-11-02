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
        board.append([" "] * COLS)
    return board


def print_board(board):
    clear_screen()
    letters = [chr(ord('A') + i) for i in range(COLS)]
    print("  " + "   ".join(letters))
    for r in range(ROWS):
        print("+" + "---+" * COLS)
        print("| " + " | ".join(board[r]) + " |")
    print("+" + "---+" * COLS)


def drop_checker(board, col, checker):
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    return False


def check_winner(board, checker):
    # horizontal
    for r in range(ROWS):
        for c in range(COLS - 3):
            if (board[r][c] == checker and board[r][c+1] == checker and
                    board[r][c+2] == checker and board[r][c+3] == checker):
                return True

    # vertical
    for r in range(ROWS - 3):
        for c in range(COLS):
            if (board[r][c] == checker and board[r+1][c] == checker and
                    board[r+2][c] == checker and board[r+3][c] == checker):
                return True

    # diagonal down-right
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if (board[r][c] == checker and board[r+1][c+1] == checker and
                    board[r+2][c+2] == checker and board[r+3][c+3] == checker):
                return True

    # diagonal up-right
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if (board[r][c] == checker and board[r-1][c+1] == checker and
                    board[r-2][c+2] == checker and board[r-3][c+3] == checker):
                return True

    return False


def full_board(board):
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == " ":
                return False
    return True


def valid_column(input_str):
    if len(input_str) != 1:
        return False
    c = input_str[0]
    if c < 'A' or c >= chr(ord('A') + COLS):
        return False
    return True


def main():
    board = create_board()
    players = CHECKERS[:PLAYERS]
    current = random.randint(0, PLAYERS - 1)
    print_board(board)

    while True:
        player = players[current]
        col_input = input(f"Player {player}, please enter a column: ")
        col_input = col_input.strip().upper()

        if not valid_column(col_input):
            continue

        col = ord(col_input) - ord('A')

        placed = drop_checker(board, col, player)
        if not placed:
            current = (current + 1) % PLAYERS
            print_board(board)
            continue

        print_board(board)

        if check_winner(board, player):
            print(f"Player {player} won!")
            break

        if full_board(board):
            print("The game is a draw!")
            break

        current = (current + 1) % PLAYERS


if __name__ == "__main__":
    main()
