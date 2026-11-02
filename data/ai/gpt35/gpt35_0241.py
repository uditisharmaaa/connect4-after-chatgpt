import os
import random

# Constants
ROWS = 6
COLUMNS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def clear_screen():
    os.system('clear')

def create_board():
    board = [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]
    return board

def print_board(board):
    clear_screen()
    # Print column headers
    headers = [chr(ord('A') + i) for i in range(COLUMNS)]
    print(" ", end=" ")
    for h in headers:
        print(f" {h}  ", end="")
    print()
    # Print board rows with separators
    for r in range(ROWS):
        print("+" + "---+" * COLUMNS)
        print("|", end="")
        for c in range(COLUMNS):
            print(f" {board[r][c]} |", end="")
        print()
    print("+" + "---+" * COLUMNS)

def is_valid_column(col_char, board):
    if len(col_char) != 1:
        return False
    col_char = col_char.upper()
    if col_char < 'A' or col_char >= chr(ord('A') + COLUMNS):
        return False
    col_index = ord(col_char) - ord('A')
    # If the top row of that column is not empty, the column is full
    return board[0][col_index] == " "

def get_column_index(col_char):
    return ord(col_char.upper()) - ord('A')

def place_checker(board, col_index, checker):
    # Place the checker in the lowest empty spot in column
    for row in range(ROWS-1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = checker
            return row, col_index
    return None  # Should not happen if checked with is_valid_column

def check_winner(board, checker):
    # Check horizontal
    for r in range(ROWS):
        for c in range(COLUMNS - 3):
            if all(board[r][c+i] == checker for i in range(4)):
                return True

    # Check vertical
    for c in range(COLUMNS):
        for r in range(ROWS - 3):
            if all(board[r+i][c] == checker for i in range(4)):
                return True

    # Check diagonal (down-right)
    for r in range(ROWS - 3):
        for c in range(COLUMNS - 3):
            if all(board[r+i][c+i] == checker for i in range(4)):
                return True

    # Check diagonal (down-left)
    for r in range(ROWS - 3):
        for c in range(3, COLUMNS):
            if all(board[r+i][c-i] == checker for i in range(4)):
                return True

    return False

def is_draw(board):
    for c in range(COLUMNS):
        if board[0][c] == " ":
            return False
    return True

def main():
    board = create_board()
    players = CHECKERS[:NUM_PLAYERS]
    current_player_index = random.randint(0, NUM_PLAYERS - 1)

    print_board(board)

    while True:
        checker = players[current_player_index]
        print(f"Player {checker}, please enter a column:")
        move = input().strip()

        # Input validation loop
        while not is_valid_column(move, board):
            if len(move) == 1 and move.upper() >= 'A' and move.upper() < chr(ord('A') + COLUMNS):
                col_idx = get_column_index(move)
                # Column is full -> turn lost
                print(f"Column {move.upper()} is full. Turn lost.")
                break
            else:
                print("Invalid input. Please enter a valid column letter:")
                move = input().strip()
        else:
            col_idx = get_column_index(move)
            # Place checker only if the column is not full
            pos = place_checker(board, col_idx, checker)
            print_board(board)

            # Check win
            if check_winner(board, checker):
                print(f"Player {checker} won!")
                break
            # Check draw
            if is_draw(board):
                print("The game is a draw!")
                break

            # Next player's turn
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            continue

        # If column full - skip turn but print board and next player
        print_board(board)
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
