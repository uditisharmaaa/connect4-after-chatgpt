import os
import random
import sys

# === CONSTANTS ===
ROWS = 6
COLUMNS = 7
MAX_COLUMNS = 26
NUM_PLAYERS = 2 # Change for more players (between 2 and 5)
PLAYER_CHECKERS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]
FOUR = 4

def clear_screen():
    os.system('clear') # use 'cls' for Windows if testing locally

def create_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    column_labels = [chr(ord('A') + i) for i in range(COLUMNS)]
    print("  " + "   ".join(column_labels))
    print('+' + '---+'*COLUMNS)
    for row in board:
        print('|' + '|'.join(' {} '.format(cell) for cell in row) + '|')
        print('+' + '---+'*COLUMNS)

def get_valid_column_input(board, current_player):
    column_labels = [chr(ord('A') + i) for i in range(COLUMNS)]
    while True:
        user_input = input(f"Player {PLAYER_CHECKERS[current_player]}, please enter a column: ").strip()
        if len(user_input) != 1 or not user_input.isalpha() or user_input.upper() not in column_labels:
            print("Invalid input! Please enter a valid column letter.")
            continue
        col = ord(user_input.upper()) - ord('A')
        if board[0][col] != " ":
            print("Column is full. You lose your turn!")
            return None # lose turn
        return col

def place_checker(board, col, checker):
    for row in range(ROWS-1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row, col

def check_win(board, checker):
    # Horizontal
    for row in range(ROWS):
        for col in range(COLUMNS - (FOUR-1)):
            if all(board[row][col + offset] == checker for offset in range(FOUR)):
                return True
    # Vertical
    for row in range(ROWS - (FOUR-1)):
        for col in range(COLUMNS):
            if all(board[row + offset][col] == checker for offset in range(FOUR)):
                return True
    # Diagonal (down-right)
    for row in range(ROWS - (FOUR-1)):
        for col in range(COLUMNS - (FOUR-1)):
            if all(board[row + offset][col + offset] == checker for offset in range(FOUR)):
                return True
    # Diagonal (up-right)
    for row in range(FOUR - 1, ROWS):
        for col in range(COLUMNS - (FOUR-1)):
            if all(board[row - offset][col + offset] == checker for offset in range(FOUR)):
                return True
    return False

def check_draw(board):
    return all(cell != " " for cell in board[0])

def main():
    board = create_board()
    current_player = random.randint(0, NUM_PLAYERS - 1)

    clear_screen()
    print_board(board)
    print(f"Player {PLAYER_CHECKERS[current_player]} starts!\n")

    while True:
        col = get_valid_column_input(board, current_player)
        if col is not None:
            row, placed_col = place_checker(board, col, PLAYER_CHECKERS[current_player])
            clear_screen()
            print_board(board)
            if check_win(board, PLAYER_CHECKERS[current_player]):
                print(f"Player {PLAYER_CHECKERS[current_player]} won!")
                break
            if check_draw(board):
                print("It's a draw!")
                break
            current_player = (current_player + 1) % NUM_PLAYERS
        else:
            # Invalid column (full), so skip turn
            current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
