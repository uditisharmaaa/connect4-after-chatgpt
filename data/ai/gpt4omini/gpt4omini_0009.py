import os
import random

# Constants for the game dimensions and players
ROWS = 6
COLS = 7
PLAYERS = ["X", "O"]  # Players can be expanded to ["X", "O", "V", "H", "M"]

# Function to create the game board
def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

# Function to print the game board
def print_board(board):
    os.system('clear')
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))  # Column headers A-G
    print("+---" * COLS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLS + "+")

# Function to validate the column input
def is_valid_input(column, board):
    if len(column) != 1 or column not in "ABCDEFGHIJKLMN":
        return False
    col_index = ord(column) - 65
    return 0 <= col_index < COLS and board[0][col_index] == " "

# Function to place the checker in the board
def place_checker(board, column, checker):
    col_index = ord(column) - 65
    for row in reversed(range(ROWS)):
        if board[row][col_index] == " ":
            board[row][col_index] = checker
            return True
    return False

# Function to check for a win
def check_win(board, checker):
    # Horizontal check
    for r in range(ROWS):
        for c in range(COLS - 3):
            if all(board[r][c + i] == checker for i in range(4)):
                return True

    # Vertical check
    for c in range(COLS):
        for r in range(ROWS - 3):
            if all(board[r + i][c] == checker for i in range(4)):
                return True

    # Diagonal check (down-right)
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if all(board[r + i][c + i] == checker for i in range(4)):
                return True

    # Diagonal check (down-left)
    for r in range(ROWS - 3):
        for c in range(3, COLS):
            if all(board[r + i][c - i] == checker for i in range(4)):
                return True

    return False

# Function to check for a draw
def check_draw(board):
    return all(board[0][c] != " " for c in range(COLS))

# Main function to run the game
def main():
    board = create_board()
    current_player = random.choice(PLAYERS)
    game_over = False

    print_board(board)

    while not game_over:
        print(f"Player {current_player}, please enter a column:")
        column = input().strip().upper()

        while not is_valid_input(column, board):
            print("Invalid input. Please enter a valid column (A-G):")
            column = input().strip().upper()

        if place_checker(board, column, current_player):
            print_board(board)
            if check_win(board, current_player):
                print(f"Player {current_player} won!")
                game_over = True
            elif check_draw(board):
                print("The game is a draw!")
                game_over = True
            current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % len(PLAYERS)]
        else:
            print("Column is full! Please choose another column.")

if __name__ == "__main__":
    main()
