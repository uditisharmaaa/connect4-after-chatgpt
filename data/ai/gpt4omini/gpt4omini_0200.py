import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')  # Clear the terminal (for Linux/Unix)
    print("  " + "   ".join(chr(65 + i) for i in range(COLUMNS)))  # Column labels A to G
    print("+---" + "+---" * (COLUMNS - 1) + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" + "+---" * (COLUMNS - 1) + "+")

def is_valid_input(column):
    return column.isalpha() and len(column) == 1 and 'A' <= column <= chr(64 + COLUMNS)

def get_bottom_free_row(board, column):
    for row in range(ROWS - 1, -1, -1):
        if board[row][column] == " ":
            return row
    return None

def check_win(board, player):
    # Check horizontal, vertical, and diagonal wins
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col + i] == player for i in range(4)):
                return True

    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == player for i in range(4)):
                return True

    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == player for i in range(4)):
                return True

    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row - i][col + i] == player for i in range(4)):
                return True

    return False

def is_draw(board):
    return all(board[0][col] != " " for col in range(COLUMNS))

def main():
    board = create_board()
    current_player = random.choice(PLAYERS[:2])  # Choose between the first two players
    
    print_board(board)
    
    while True:
        print(f"Player {current_player}, please enter a column:")
        column_input = input().strip().upper()

        while not is_valid_input(column_input):
            print("Invalid input. Please enter a valid column (A to {}):".format(chr(64 + COLUMNS)))
            column_input = input().strip().upper()

        column = ord(column_input) - 65

        # Check if column has space
        row = get_bottom_free_row(board, column)
        if row is None:
            print("Column is full. Choose another column.")
            continue  # Skip turn without changing current_player

        board[row][column] = current_player
        print_board(board)

        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            break

        if is_draw(board):
            print("The game is a draw!")
            break

        # Switch to the next player
        current_index = PLAYERS.index(current_player)
        current_player = PLAYERS[(current_index + 1) % len(PLAYERS[:2])]

if __name__ == "__main__":
    main()
