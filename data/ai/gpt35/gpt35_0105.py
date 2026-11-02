import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_COUNT = 4

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    # Print column labels
    labels = [chr(ord('A') + i) for i in range(len(board[0]))]
    print(" ", end=" ")
    for label in labels:
        print(f"  {label} ", end="")
    print()
    line = "+---" * len(board[0]) + "+"
    # Print board
    for row in board:
        print(line)
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
    print(line)

def valid_input(user_input, cols):
    if len(user_input) != 1:
        return False
    letter = user_input.upper()
    if letter < 'A' or letter >= chr(ord('A') + cols):
        return False
    return True

def column_index(letter):
    return ord(letter.upper()) - ord('A')

def place_checker(board, col, checker):
    # place checker in lowest empty spot in col
    for row in reversed(range(len(board))):
        if board[row][col] == " ":
            board[row][col] = checker
            return row
    # column full
    return -1

def check_win(board, row, col, checker):
    directions = [
        (0,1),  # horizontal right
        (1,0),  # vertical down
        (1,1),  # diagonal down-right
        (1,-1)  # diagonal down-left
    ]
    for dr, dc in directions:
        count = 1
        # check forward direction
        r, c = row + dr, col + dc
        while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # check backward direction
        r, c = row - dr, col - dc
        while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        if count >= WIN_COUNT:
            return True
    return False

def board_full(board):
    for col in range(len(board[0])):
        if board[0][col] == " ":
            return False
    return True

def main():
    board = create_board(ROWS, COLS)
    players = CHECKERS[:PLAYERS]
    current = random.randint(0, PLAYERS -1)
    while True:
        print_board(board)
        print(f"Player {players[current]}, please enter a column:")

        user_input = input().strip().upper()
        if not valid_input(user_input, COLS):
            continue  # Invalid input, ask again
        col = column_index(user_input)
        row = place_checker(board, col, players[current])
        if row == -1:
            # Column full, player loses turn
            current = (current + 1) % PLAYERS
            continue

        if check_win(board, row, col, players[current]):
            print_board(board)
            print(f"Player {players[current]} won!")
            break
        if board_full(board):
            print_board(board)
            print("The game is a draw!")
            break

        current = (current + 1) % PLAYERS

if __name__ == "__main__":
    main()
