import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')  # Clear command for Unix/Linux 
    header = "  " + "   ".join([chr(65+i) for i in range(COLUMNS)])
    print(header)
    print("+---" * COLUMNS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

def is_valid_column(column):
    if 0 <= column < COLUMNS:
        return True
    return False

def is_column_full(board, column):
    return board[0][column] != " "

def drop_checker(board, column, checker):
    for row in reversed(range(ROWS)):
        if board[row][column] == " ":
            board[row][column] = checker
            return True
    return False

def check_winner(board, checker):
    # Horizontal check
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col+i] == checker for i in range(4)):
                return True

    # Vertical check
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row+i][col] == checker for i in range(4)):
                return True

    # Diagonal checks (bottom-left to top-right)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row+i][col+i] == checker for i in range(4)):
                return True

    # Diagonal checks (top-left to bottom-right)
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row-i][col+i] == checker for i in range(4)):
                return True

    return False

def is_draw(board):
    return all(board[0][col] != " " for col in range(COLUMNS))

def main():
    board = create_board()
    current_player = random.randint(0, PLAYERS - 1)
    print_board(board)

    while True:
        current_checker = CHECKERS[current_player]
        print(f"Player {current_checker}, please enter a column:")
        user_input = input().strip().upper()

        if user_input.isalpha() and len(user_input) == 1:
            column = ord(user_input) - 65
            if is_valid_column(column):
                if not is_column_full(board, column):
                    if drop_checker(board, column, current_checker):
                        print_board(board)
                        if check_winner(board, current_checker):
                            print(f"Player {current_checker} won!")
                            break
                        elif is_draw(board):
                            print("The game is a draw!")
                            break
                        current_player = (current_player + 1) % PLAYERS
                else:
                    print("Column is full! Turn lost.")
            else:
                print("Invalid column! Please try again.")
        else:
            print("Invalid input! Please try again.")

if __name__ == "__main__":
    main()
