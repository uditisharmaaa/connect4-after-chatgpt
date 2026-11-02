import os
import random

# Constants
ROWS = 6
COLUMNS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_COUNT = 4

def clear_screen():
    os.system('clear')

def create_board(rows, columns):
    board = [[" " for _ in range(columns)] for _ in range(rows)]
    return board

def print_board(board):
    clear_screen()
    # Print column labels
    labels = "  "
    for i in range(len(board[0])):
        labels += " " + chr(ord('A') + i) + "  "
    print(labels)
    # Print board
    for row in board:
        print("+" + "---+" * len(row))
        row_str = "|"
        for cell in row:
            row_str += " " + cell + " |"
        print(row_str)
    print("+" + "---+" * len(board[0]))

def get_valid_input(current_player, board):
    while True:
        choice = input(f"Player {current_player}, please enter a column: ").strip()
        if len(choice) != 1 or not choice.isalpha():
            print("Invalid input. Please enter a single letter corresponding to a column.")
            continue
        col = ord(choice.upper()) - ord('A')
        if col < 0 or col >= len(board[0]):
            print("Invalid column. Please enter a letter within the board columns.")
            continue
        if board[0][col] != " ":
            # Column full, lose turn as per assignment
            return None
        return col

def place_checker(board, col, checker):
    # Place checker from bottom row upwards
    for row in range(len(board)-1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row, col
    # Column is full - should not happen if checked before
    return None, None

def check_line(board, start_row, start_col, delta_row, delta_col, checker):
    count = 0
    row = start_row
    col = start_col
    while 0 <= row < len(board) and 0 <= col < len(board[0]):
        if board[row][col] == checker:
            count += 1
            if count == WIN_COUNT:
                return True
        else:
            count = 0
        row += delta_row
        col += delta_col
    return False

def check_win(board, checker):
    rows = len(board)
    cols = len(board[0])
    # Check horizontal lines
    for row in range(rows):
        if check_line(board, row, 0, 0, 1, checker):
            return True
    # Check vertical lines
    for col in range(cols):
        if check_line(board, 0, col, 1, 0, checker):
            return True
    # Check diagonal (down-right)
    for row in range(rows - WIN_COUNT +1):
        for col in range(cols - WIN_COUNT +1):
            count = 0
            for i in range(WIN_COUNT):
                if board[row+i][col+i] == checker:
                    count +=1
                else:
                    break
            if count == WIN_COUNT:
                return True
    # Check diagonal (down-left)
    for row in range(rows - WIN_COUNT +1):
        for col in range(WIN_COUNT -1, cols):
            count = 0
            for i in range(WIN_COUNT):
                if board[row+i][col - i] == checker:
                    count +=1
                else:
                    break
            if count == WIN_COUNT:
                return True
    return False

def check_draw(board):
    # If top row has no empty cell, board is full
    for cell in board[0]:
        if cell == " ":
            return False
    return True

def main():
    board = create_board(ROWS, COLUMNS)
    players = CHECKERS[:NUM_PLAYERS]
    current_index = random.randint(0, NUM_PLAYERS -1)
    print_board(board)

    while True:
        current_player = players[current_index]
        col = get_valid_input(current_player, board)
        if col is None:
            # Lose turn due to full column
            print(f"Column is full. Player {current_player} loses the turn.")
        else:
            row, col_placed = place_checker(board, col, current_player)
            print_board(board)

            if check_win(board, current_player):
                print(f"Player {current_player} won!")
                break
            if check_draw(board):
                print("The game is a draw.")
                break

        current_index = (current_index +1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
