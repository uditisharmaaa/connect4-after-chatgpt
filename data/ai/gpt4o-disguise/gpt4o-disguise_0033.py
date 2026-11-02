import os
import random

ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    print("  " + "   ".join([chr(ord('A') + i) for i in range(COLS)]))
    print("+---" * COLS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLS + "+")

def is_valid_move(col, board):
    if col < 0 or col >= COLS:
        return False
    return board[0][col] == " "

def make_move(col, player, board):
    for row in range(ROWS-1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = player
            break

def check_winner(board):
    for r in range(ROWS):
        for c in range(COLS - 3):
            if board[r][c] == board[r][c + 1] == board[r][c + 2] == board[r][c + 3] != " ":
                return True

    for r in range(ROWS - 3):
        for c in range(COLS):
            if board[r][c] == board[r + 1][c] == board[r + 2][c] == board[r + 3][c] != " ":
                return True

    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if board[r][c] == board[r + 1][c + 1] == board[r + 2][c + 2] == board[r + 3][c + 3] != " ":
                return True

    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if board[r][c] == board[r - 1][c + 1] == board[r - 2][c + 2] == board[r - 3][c + 3] != " ":
                return True

    return False

def check_draw(board):
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True

def main():
    board = create_board()
    current_player_idx = random.randint(0, PLAYERS - 1)
    current_player = CHECKERS[current_player_idx]

    while True:
        print_board(board)
        print(f"Player {current_player}, please enter a column:")
        move = input().strip()

        if len(move) == 1 and 'A' <= move <= 'Z':
            col = ord(move) - ord('A')
            if is_valid_move(col, board):
                make_move(col, current_player, board)
                if check_winner(board):
                    print_board(board)
                    print(f"Player {current_player} won!")
                    break
                elif check_draw(board):
                    print_board(board)
                    print("The game is a draw!")
                    break
                current_player_idx = (current_player_idx + 1) % PLAYERS
                current_player = CHECKERS[current_player_idx]
            else:
                print("Column is full, choose another one.")
        else:
            print("Invalid input, enter a valid column letter.")

if __name__ == "__main__":
    main()
