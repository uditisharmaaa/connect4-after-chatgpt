import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_COUNT = 4

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    board = [[" " for _ in range(cols)] for _ in range(rows)]
    return board

def print_board(board):
    clear_screen()
    # Print column labels
    labels = [chr(ord('A') + i) for i in range(len(board[0]))]
    print("  " + "   ".join(labels))
    # Print board rows
    for row in range(len(board)):
        print("+" + "---+" * len(board[0]))
        print("| " + " | ".join(board[row]) + " |")
    print("+" + "---+" * len(board[0]))

def is_valid_column_input(col_input, cols):
    if len(col_input) != 1:
        return False
    if not ('A' <= col_input <= chr(ord('A') + cols - 1)):
        return False
    return True

def get_column_index(col_input):
    return ord(col_input) - ord('A')

def place_checker(board, col_idx, checker):
    # Find the lowest empty spot in column
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_idx] == " ":
            board[row][col_idx] = checker
            return True
    # Column is full
    return False

def check_win(board, checker):
    rows = len(board)
    cols = len(board[0])

    # Horizontal check
    for r in range(rows):
        count = 0
        for c in range(cols):
            if board[r][c] == checker:
                count += 1
                if count == WIN_COUNT:
                    return True
            else:
                count = 0

    # Vertical check
    for c in range(cols):
        count = 0
        for r in range(rows):
            if board[r][c] == checker:
                count += 1
                if count == WIN_COUNT:
                    return True
            else:
                count = 0

    # Diagonal check (\)
    for r in range(rows - WIN_COUNT + 1):
        for c in range(cols - WIN_COUNT + 1):
            count = 0
            for i in range(WIN_COUNT):
                if board[r + i][c + i] == checker:
                    count += 1
                else:
                    break
            if count == WIN_COUNT:
                return True

    # Diagonal check (/)
    for r in range(WIN_COUNT - 1, rows):
        for c in range(cols - WIN_COUNT + 1):
            count = 0
            for i in range(WIN_COUNT):
                if board[r - i][c + i] == checker:
                    count += 1
                else:
                    break
            if count == WIN_COUNT:
                return True

    return False

def check_draw(board):
    for c in range(len(board[0])):
        if board[0][c] == " ":
            return False
    return True

def main():
    board = create_board(ROWS, COLS)
    players = CHECKERS[:NUM_PLAYERS]
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)

    while True:
        print_board(board)
        current_checker = players[current_player_idx]
        print(f"Player {current_checker}, please enter a column:")

        while True:
            col_input = input().strip().upper()
            if not is_valid_column_input(col_input, COLS):
                print("Invalid input. Please enter a valid column letter:")
                continue
            col_idx = get_column_index(col_input)
            placed = place_checker(board, col_idx, current_checker)
            if not placed:
                # Column full, lose turn
                break
            else:
                # Successfully placed
                break

        # If checker placed, check for win or draw
        if placed:
            if check_win(board, current_checker):
                print_board(board)
                print(f"Player {current_checker} won!")
                break
            if check_draw(board):
                print_board(board)
                print("The game is a draw!")
                break

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
