import os
import random

# Constants for board dimensions and number of players
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

# Creating and initializing the board
def create_board(rows, columns):
    return [[' ' for _ in range(columns)] for _ in range(rows)]

# Printing the board
def print_board(board):
    os.system('clear')
    column_labels = ' '.join(chr(65 + i) for i in range(len(board[0])))
    print(f"  {column_labels}")
    print("+---" * len(board[0]) + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * len(board[0]) + "+")

# Check for a valid move
def is_valid_move(board, column):
    return board[0][column] == ' '

# Place the checker in the lowest available row in the specified column
def place_checker(board, column, checker):
    for row in reversed(board):
        if row[column] == ' ':
            row[column] = checker
            break

# Check for a win in the game
def check_winner(board, checker):
    for r in range(ROWS):
        for c in range(COLUMNS):
            if c + 3 < COLUMNS and all(board[r][c+i] == checker for i in range(4)):
                return True
            if r + 3 < ROWS and all(board[r+i][c] == checker for i in range(4)):
                return True
            if r + 3 < ROWS and c + 3 < COLUMNS and all(board[r+i][c+i] == checker for i in range(4)):
                return True
            if r - 3 >= 0 and c + 3 < COLUMNS and all(board[r-i][c+i] == checker for i in range(4)):
                return True
    return False

# Check for a draw in the game
def check_draw(board):
    return all(row[0] != ' ' for row in board)

# Main game loop
def play_game():
    board = create_board(ROWS, COLUMNS)
    current_player = random.randint(0, PLAYERS - 1)
    print_board(board)

    while True:
        print(f"Player {CHECKERS[current_player]}, please enter a column:")
        move = input().strip().upper()

        if len(move) != 1 or not move.isalpha():
            print("Invalid input. Please enter a valid column letter.")
            continue

        column = ord(move) - 65

        if column < 0 or column >= COLUMNS:
            print("Invalid column. Please try again.")
            continue

        if not is_valid_move(board, column):
            print("Column full. Try another column.")
            continue

        place_checker(board, column, CHECKERS[current_player])
        print_board(board)

        if check_winner(board, CHECKERS[current_player]):
            print(f"Player {CHECKERS[current_player]} won!")
            break
        if check_draw(board):
            print("The game is a draw!")
            break

        current_player = (current_player + 1) % PLAYERS

if __name__ == '__main__':
    play_game()
