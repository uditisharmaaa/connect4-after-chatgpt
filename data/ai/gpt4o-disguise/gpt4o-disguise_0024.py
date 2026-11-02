import random
import os

MAX_COLUMNS = 26
NUM_ROWS = 6
NUM_COLUMNS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    os.system('clear')
    print("  " + "   ".join(chr(65 + i) for i in range(len(board[0]))))
    print("+" + "---+" * len(board[0]))
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * len(board[0]))

def check_win(board, player):
    # Check horizontal
    for row in board:
        for col in range(NUM_COLUMNS - 3):
            if row[col] == row[col+1] == row[col+2] == row[col+3] == player:
                return True

    # Check vertical
    for col in range(NUM_COLUMNS):
        for row in range(NUM_ROWS - 3):
            if board[row][col] == board[row+1][col] == board[row+2][col] == board[row+3][col] == player:
                return True

    # Check diagonal (\ direction)
    for row in range(NUM_ROWS - 3):
        for col in range(NUM_COLUMNS - 3):
            if board[row][col] == board[row+1][col+1] == board[row+2][col+2] == board[row+3][col+3] == player:
                return True

    # Check diagonal (/ direction)
    for row in range(3, NUM_ROWS):
        for col in range(NUM_COLUMNS - 3):
            if board[row][col] == board[row-1][col+1] == board[row-2][col+2] == board[row-3][col+3] == player:
                return True

    return False

def check_draw(board):
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True

def main():
    board = create_board(NUM_ROWS, NUM_COLUMNS)
    print_board(board)

    players = CHECKERS[:NUM_PLAYERS]
    current_player = random.choice(players)

    while True:
        col_input = input(f"Player {current_player}, please enter a column: ").strip().upper()

        if col_input not in [chr(65+i) for i in range(NUM_COLUMNS)]:
            print("Invalid column. Try again.")
            continue

        col_index = ord(col_input) - 65
        if board[0][col_index] != " ":
            print("Column is full. You lose your turn.")
            current_player = players[(players.index(current_player) + 1) % len(players)]
            continue

        for row in range(NUM_ROWS-1, -1, -1):
            if board[row][col_index] == " ":
                board[row][col_index] = current_player
                break

        print_board(board)

        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            break

        if check_draw(board):
            print("The game is a draw!")
            break

        current_player = players[(players.index(current_player) + 1) % len(players)]

main()
