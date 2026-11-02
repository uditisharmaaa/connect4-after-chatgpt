import os
import random

ROWS = 6
COLS = 7
COL_LABELS = ['A','B','C','D','E','F','G']
PLAYERS = ['X','O','V','H','M']  # max 5 players

def clear_screen():
    os.system('clear')

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    print(" " + " ".join(COL_LABELS))
    for row in board:
        print("|" + "|".join(row) + "|")
    print("-" * (COLS * 2 + 1))

def get_move(player, board):
    while True:
        move = input(f"Player {player}, choose column (A-G): ").upper()
        if move not in COL_LABELS:
            print("Invalid column, please choose A-G.")
            continue
        col = COL_LABELS.index(move)
        if board[0][col] != ' ':
            print("That column is full! Try another one.")
            continue
        return col

def make_move(board, col, player):
    for row in reversed(range(ROWS)):
        if board[row][col] == ' ':
            board[row][col] = player
            return row, col

def check_win(board, player):
    # horizontal check
    for r in range(ROWS):
        for c in range(COLS - 3):
            if all(board[r][c+i] == player for i in range(4)):
                return True
    # vertical check
    for c in range(COLS):
        for r in range(ROWS - 3):
            if all(board[r+i][c] == player for i in range(4)):
                return True
    # diagonal down-right check
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if all(board[r+i][c+i] == player for i in range(4)):
                return True
    # diagonal up-right check
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if all(board[r - i][c + i] == player for i in range(4)):
                return True
    return False

def check_draw(board):
    return all(board[0][c] != ' ' for c in range(COLS))

def main():
    clear_screen()
    print("Welcome to Connect 4!")
    while True:
        try:
            num_players = int(input("Enter number of players (2-5): "))
            if 2 <= num_players <= 5:
                break
            else:
                print("Please enter a number between 2 and 5.")
        except ValueError:
            print("That's not a valid number.")

    players = PLAYERS[:num_players]
    current_player_index = random.randint(0, num_players - 1)

    board = create_board()
    while True:
        clear_screen()
        print_board(board)
        player = players[current_player_index]
        col = get_move(player, board)
        make_move(board, col, player)
        if check_win(board, player):
            clear_screen()
            print_board(board)
            print(f"Player {player} wins! Congratulations!")
            break
        if check_draw(board):
            clear_screen()
            print_board(board)
            print("It's a draw!")
            break
        current_player_index = (current_player_index + 1) % num_players

if __name__ == "__main__":
    main()
