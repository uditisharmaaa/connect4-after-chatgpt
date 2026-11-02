import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

# Function to create the board
def create_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

# Function to print the board
def print_board(board):
    os.system('clear')
    print("  " + "   ".join(chr(65 + i) for i in range(COLUMNS)))
    for row in board:
        print("+---" * COLUMNS + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * COLUMNS + "+")

# Function to check if a move is valid
def is_valid_move(board, column):
    return board[0][column] == " "

# Function to make a move
def make_move(board, column, checker):
    for row in range(ROWS - 1, -1, -1):
        if board[row][column] == " ":
            board[row][column] = checker
            break

# Function to check for a win condition
def check_for_win(board, checker):
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if board[row][col] == checker and board[row][col + 1] == checker and board[row][col + 2] == checker and board[row][col + 3] == checker:
                return True

    # Check vertical
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if board[row][col] == checker and board[row + 1][col] == checker and board[row + 2][col] == checker and board[row + 3][col] == checker:
                return True

    # Check diagonal (down-right and down-left)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if board[row][col] == checker and board[row + 1][col + 1] == checker and board[row + 2][col + 2] == checker and board[row + 3][col + 3] == checker:
                return True
        for col in range(3, COLUMNS):
            if board[row][col] == checker and board[row + 1][col - 1] == checker and board[row + 2][col - 2] == checker and board[row + 3][col - 3] == checker:
                return True

    return False

# Function to check for a draw condition
def check_for_draw(board):
    for col in range(COLUMNS):
        if board[0][col] == " ":
            return False
    return True

# Main Function
def main():
    board = create_board()
    print_board(board)
    
    current_player = random.randint(0, PLAYERS - 1)
    game_over = False

    while not game_over:
        print(f"Player {CHECKERS[current_player % PLAYERS]}, please enter a column:")
        move = input().strip().upper()
        
        if len(move) != 1 or not ('A' <= move <= chr(65 + COLUMNS - 1)):
            print("Invalid input. Please enter a valid column.")
            continue
        
        column = ord(move) - 65

        if not is_valid_move(board, column):
            print("Column is full. Please choose another column.")
            continue

        make_move(board, column, CHECKERS[current_player % PLAYERS])
        print_board(board)

        if check_for_win(board, CHECKERS[current_player % PLAYERS]):
            print(f"Player {CHECKERS[current_player % PLAYERS]} won!")
            game_over = True
        elif check_for_draw(board):
            print("The game is a draw!")
            game_over = True
        else:
            current_player += 1

if __name__ == "__main__":
    main()
