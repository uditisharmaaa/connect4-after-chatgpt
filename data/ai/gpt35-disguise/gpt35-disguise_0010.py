import os
import random

ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def clear_screen():
    os.system("clear")

def create_board():
    board = []
    for _ in range(ROWS):
        row = [" "] * COLS
        board.append(row)
    return board

def print_board(board):
    clear_screen()
    header = "  "
    for i in range(COLS):
        header += chr(ord("A") + i) + "   "
    print(header)
    print("+---" * COLS + "+")
    for row in board:
        line = "|"
        for cell in row:
            line += " " + cell + " |"
        print(line)
        print("+---" * COLS + "+")

def get_player_input(player):
    while True:
        col = input(f"Player {player}, please enter a column: ").upper()
        if len(col) != 1:
            continue
        if col < "A" or col >= chr(ord("A") + COLS):
            continue
        return ord(col) - ord("A")

def place_checker(board, col, checker):
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return True
    return False

def check_winner(board, checker):
    # horizontal check
    for r in range(ROWS):
        for c in range(COLS - 3):
            if board[r][c] == checker and board[r][c+1] == checker and board[r][c+2] == checker and board[r][c+3] == checker:
                return True
    # vertical check
    for c in range(COLS):
        for r in range(ROWS - 3):
            if board[r][c] == checker and board[r+1][c] == checker and board[r+2][c] == checker and board[r+3][c] == checker:
                return True
    # diagonal down-right
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if board[r][c] == checker and board[r+1][c+1] == checker and board[r+2][c+2] == checker and board[r+3][c+3] == checker:
                return True
    # diagonal up-right
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if board[r][c] == checker and board[r-1][c+1] == checker and board[r-2][c+2] == checker and board[r-3][c+3] == checker:
                return True
    return False

def board_full(board):
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == " ":
                return False
    return True

def main():
    board = create_board()
    players = PLAYERS
    checkers = CHECKERS[:players]
    current = random.randint(0, players -1)
    print_board(board)
    while True:
        checker = checkers[current]
        col = get_player_input(checker)
        if not place_checker(board, col, checker):
            # lose turn if column full
            current = (current +1) % players
            print_board(board)
            continue
        print_board(board)
        if check_winner(board, checker):
            print(f"Player {checker} won!")
            break
        if board_full(board):
            print("The game is a draw.")
            break
        current = (current +1) % players

if __name__ == "__main__":
    main()
