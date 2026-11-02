import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def clear_screen():
    os.system('clear')

def create_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    # Print column labels
    labels = [chr(ord('A') + i) for i in range(COLUMNS)]
    print("  " + "   ".join(labels))
    # Print board rows with separators
    for row in range(ROWS):
        print("+---" * COLUMNS + "+")
        row_str = "|"
        for col in range(COLUMNS):
            row_str += " " + board[row][col] + " |"
        print(row_str)
    print("+---" * COLUMNS + "+")

def input_column(current_player):
    while True:
        col_input = input(f"Player {CHECKERS[current_player]}, please enter a column: ").strip().upper()
        if len(col_input) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        col = ord(col_input) - ord('A')
        if col < 0 or col >= COLUMNS:
            print("Invalid column letter. Please enter a valid column.")
            continue
        return col

def place_checker(board, col, checker):
    # Place checker in given column; return True if placed, False if column full
    for row in range(ROWS-1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    return False

def check_winner(board, checker):
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True
    # Check vertical
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == checker for i in range(4)):
                return True
    # Check diagonal down-right
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True
    # Check diagonal up-right
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True
    return False

def check_draw(board):
    for row in board:
        if " " in row:
            return False
    return True

def main():
    board = create_board()
    players = CHECKERS[:PLAYERS]
    current_player = random.randint(0, PLAYERS - 1)
    print_board(board)

    while True:
        col = input_column(current_player)
        placed = place_checker(board, col, players[current_player])
        if not placed:
            # The turn is lost if column full
            print("Column full! You lose your turn.")
            # pause before next turn
            input("Press Enter to continue...")
            current_player = (current_player + 1) % PLAYERS
            print_board(board)
            continue
        print_board(board)
        if check_winner(board, players[current_player]):
            print(f"Player {players[current_player]} won!")
            break
        if check_draw(board):
            print("The game is a draw!")
            break
        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
