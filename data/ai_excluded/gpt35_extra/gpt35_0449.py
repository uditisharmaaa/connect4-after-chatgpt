import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYER_COUNT = 2
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_COUNT = 4

def clear_screen():
    os.system('clear')

def create_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    # Print column headers
    letters = [chr(ord('A') + i) for i in range(COLUMNS)]
    print("  " + "   ".join(letters))
    # Print board rows
    for row in board:
        print("+" + "---+" * COLUMNS)
        print("| " + " | ".join(row) + " |")
    print("+" + "---+" * COLUMNS)

def get_valid_column(board, player):
    letters = [chr(ord('A') + i) for i in range(COLUMNS)]
    while True:
        choice = input(f"Player {player}, please enter a column: ").strip().upper()
        if len(choice) != 1 or choice not in letters:
            continue
        col = ord(choice) - ord('A')
        # Check if column is full
        if board[0][col] != " ":
            # Player loses turn if column full
            print("Column is full. You lose your turn.")
            return None
        else:
            return col

def place_checker(board, col, checker):
    # Place checker in lowest empty row in the given column
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row, col

def check_win(board, checker):
    # Horizontal check
    for r in range(ROWS):
        for c in range(COLUMNS - WIN_COUNT + 1):
            if all(board[r][c + i] == checker for i in range(WIN_COUNT)):
                return True
    # Vertical check
    for c in range(COLUMNS):
        for r in range(ROWS - WIN_COUNT + 1):
            if all(board[r + i][c] == checker for i in range(WIN_COUNT)):
                return True
    # Diagonal (down-right) check
    for r in range(ROWS - WIN_COUNT + 1):
        for c in range(COLUMNS - WIN_COUNT + 1):
            if all(board[r + i][c + i] == checker for i in range(WIN_COUNT)):
                return True
    # Diagonal (down-left) check
    for r in range(ROWS - WIN_COUNT + 1):
        for c in range(WIN_COUNT - 1, COLUMNS):
            if all(board[r + i][c - i] == checker for i in range(WIN_COUNT)):
                return True
    return False

def check_draw(board):
    # If no empty spaces in top row, and no win, it's a draw
    for c in range(COLUMNS):
        if board[0][c] == " ":
            return False
    return True

def main():
    board = create_board()
    players = CHECKERS[:PLAYER_COUNT]

    current_player_index = random.randint(0, PLAYER_COUNT - 1)

    print_board(board)

    while True:
        current_checker = players[current_player_index]
        col = get_valid_column(board, current_checker)
        if col is not None:
            place_checker(board, col, current_checker)
            print_board(board)
            if check_win(board, current_checker):
                print(f"Player {current_checker} won!")
                break
            if check_draw(board):
                print("The game is a draw!")
                break
        else:
            # Column full, lose turn and just continue to next player
            print_board(board)
        # Next player's turn
        current_player_index = (current_player_index + 1) % PLAYER_COUNT

if __name__ == "__main__":
    main()
