import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    os.system('clear')
    print("  " + "   ".join(chr(65 + col) for col in range(len(board[0]))))
    print("+" + ---+ * len(board[0]))
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + ---+ * len(board[0]))

def get_player_checker(player_index):
    return CHECKERS[player_index % len(CHECKERS)]

def is_valid_column(column, board):
    return0 <= column < len(board[0]) and board[0][column] == " "

def drop_checker(board, column, checker):
    for row in range(len(board) - 1, -1, -1):
        if board[row][column] == " ":
            board[row][column] = checker
            return True
    return False

def check_win(board, checker):
    # Check horizontal
    for row in board:
        for col in range(len(row) - 3):
            if row[col] == row[col + 1] == row[col + 2] == row[col + 3] == checker:
                return True

    # Check vertical
    for col in range(len(board[0])):
        for row in range(len(board) - 3):
            if board[row][col] == board[row + 1][col] == board[row + 2][col] == board[row + 3][col] == checker:
                return True

    # Check diagonal (down-right)
    for row in range(len(board) - 3):
        for col in range(len(board[0]) - 3):
            if board[row][col] == board[row + 1][col + 1] == board[row + 2][col + 2] == board[row + 3][col + 3] == checker:
                return True

    # Check diagonal (up-right)
    for row in range(3, len(board)):
        for col in range(len(board[0]) - 3):
            if board[row][col] == board[row - 1][col + 1] == board[row - 2][col + 2] == board[row - 3][col + 3] == checker:
                return True

    return False

def check_draw(board):
    return all(board[0][col] != " " for col in range(len(board[0])))

def main():
    board = create_board(ROWS, COLS)
    current_player = random.randint(0, PLAYERS - 1)
    
    while True:
        print_board(board)
        checker = get_player_checker(current_player)
        print(f"Player {checker}, please enter a column:, end=")
        
        column_input = input().strip().upper()
        if len(column_input) != 1 or not column_input.isalpha() or not is_valid_column(ord(column_input) - 65, board):
            print("Invalid input. Please try again.")
            continue
        
        column = ord(column_input) - 65      if not drop_checker(board, column, checker):
            print("Column is full. Please try again.")
            continue
        
        if check_win(board, checker):
            print_board(board)
            print(f"Player {checker} won!")
            break
        
        if check_draw(board):
            print_board(board)
            print("It's a draw!")
            break
        
        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
