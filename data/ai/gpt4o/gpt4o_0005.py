import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYER_COUNT = 2  # Can be 2 to 5
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    os.system('clear')
    column_labels = "  ".join(chr(65 + i) for i in range(COLUMNS))
    print(f"  {column_labels}")
    print("+" + "---+" * COLUMNS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLUMNS)

def valid_column_choice(choice):
    return choice.isalpha() and 0 <= ord(choice) - 65 < COLUMNS

def is_column_full(board, column):
    return board[0][column] != " "

def place_checker(board, column, checker):
    for row in reversed(range(ROWS)):
        if board[row][column] == " ":
            board[row][column] = checker
            return

def check_win(board, checker):
    # Horizontal, Vertical, Diagonal checks
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True
    for row in range(ROWS - 3):
        for col in range(COLUMNS):
            if all(board[row + i][col] == checker for i in range(4)):
                return True
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True
            if all(board[row + 3 - i][col + i] == checker for i in range(4)):
                return True
    return False

def check_draw(board):
    return all(cell != " " for cell in board[0])

def main():
    board = create_board(ROWS, COLUMNS)
    print_board(board)
    
    current_player = random.choice(range(PLAYER_COUNT))
    while True:
        player_checker = CHECKERS[current_player]
        print(f"Player {player_checker}, please enter a column:")
        choice = input().upper()

        if not valid_column_choice(choice):
            print("Invalid input. Try again.")
            continue

        column = ord(choice) - 65

        if is_column_full(board, column):
            print("Column is full. Try another.")
            continue

        place_checker(board, column, player_checker)
        print_board(board)

        if check_win(board, player_checker):
            print(f"Player {player_checker} won!")
            break
        elif check_draw(board):
            print("The game is a draw!")
            break

        current_player = (current_player + 1) % PLAYER_COUNT

if __name__ == "__main__":
    main()
