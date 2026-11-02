import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
WINNING_CHECKERS = 4

def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    print("  A", end=" ")
    for col in range(1, COLS):
        print(chr(ord("A") + col), end=" ")
    print("\n+---" + "+---" * (COLS - 1))
    for row in board:
        print("|   ", end="")
        for col in row:
            print(f"| {col} ", end="")
        print("|")
        print("+---" + "+---" * (COLS - 1))

def get_player_checker(player):
    return CHECKERS[player - 1]

def get_column(board, player):
    while True:
        col = input(f"Player {get_player_checker(player)}, please enter a column: ")
        if len(col)!= 1 or not col.isalpha():
            print("Invalid input. Please enter a single letter.")
        elif ord(col) - ord("A") < 0 or ord(col) - ord("A") >= COLS:
            print("Invalid input. Please enter a column between A and", chr(ord("A") + COLS - 1))
        else:
            col = ord(col) - ord("A")
            if board[0][col]!= " ":
                print("Column is full. Please choose another column.")
            else:
                for row in range(ROWS - 1, -1, -1):
                    if board[row][col] == " ":
                        board[row][col] = get_player_checker(player)
                        return

def check_win(board):
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - WINNING_CHECKERS + 1):
            if board[row][col]!= " ":
                player = board[row][col]
                for i in range(WINNING_CHECKERS):
                    if board[row][col + i]!= player:
                        break
                else:
                    return player

    # Check vertical
    for row in range(ROWS - WINNING_CHECKERS + 1):
        for col in range(COLS):
            if board[row][col]!= " ":
                player = board[row][col]
                for i in range(WINNING_CHECKERS):
                    if board[row + i][col]!= player:
                        break
                else:
                    return player

    # Check diagonal (top-left to bottom-right)
    for row in range(ROWS - WINNING_CHECKERS + 1):
        for col in range(COLS - WINNING_CHECKERS + 1):
            if board[row][col]!= " ":
                player = board[row][col]
                for i in range(WINNING_CHECKERS):
                    if board[row + i][col + i]!= player:
                        break
                else:
                    return player

    # Check diagonal (bottom-left to top-right)
    for row in range(WINNING_CHECKERS - 1, ROWS):
        for col in range(COLS - WINNING_CHECKERS + 1):
            if board[row][col]!= " ":
                player = board[row][col]
                for i in range(WINNING_CHECKERS):
                    if board[row - i][col + i]!= player:
                        break
                else:
                    return player

    return None

def check_draw(board):
    return all(board[0][col]!= " " for col in range(COLS))

def main():
    board = create_board()
    print_board(board)
    players = list(range(1, PLAYERS + 1))
    random.shuffle(players)
    for turn in range(ROWS * COLS):
        player = players[turn % PLAYERS]
        get_column(board, player)
        print_board(board)
        winner = check_win(board)
        if winner:
            print(f"Player {winner} won!")
            return
        if check_draw(board):
            print("It's a draw!")
            return

if __name__ == "__main__":
    main()
