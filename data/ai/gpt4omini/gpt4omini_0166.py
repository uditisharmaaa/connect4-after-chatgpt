import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O']  # You can extend this to ['X', 'O', 'V', 'H', 'M'] for more players

# Function to create the game board
def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

# Function to print the board
def print_board(board):
    os.system('clear')  # Clear the screen
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))  # Column labels A-G
    print("+" + "---+" * COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)

# Function to check for a win
def check_win(board):
    # Check horizontal, vertical, and diagonal
    for r in range(ROWS):
        for c in range(COLS - 3):
            if board[r][c] != ' ' and all(board[r][c] == board[r][c+i] for i in range(4)):
                return True
    for r in range(ROWS - 3):
        for c in range(COLS):
            if board[r][c] != ' ' and all(board[r][c] == board[r+i][c] for i in range(4)):
                return True
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if board[r][c] != ' ' and all(board[r][c] == board[r+i][c+i] for i in range(4)):
                return True
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if board[r][c] != ' ' and all(board[r][c] == board[r-i][c+i] for i in range(4)):
                return True
    return False

# Function to check for a draw
def check_draw(board):
    return all(cell != ' ' for row in board for cell in row)

# Function to place a checker
def place_checker(board, column, checker):
    for row in range(ROWS - 1, -1, -1):  # Start from the bottom
        if board[row][column] == ' ':
            board[row][column] = checker
            return True
    return False

# Main game function
def connect_4():
    board = create_board()
    current_player_index = random.randint(0, len(PLAYERS) - 1)  # Randomly select first player

    while True:
        print_board(board)
        current_checker = PLAYERS[current_player_index]
        column = input(f"Player {current_checker}, please enter a column (A-G): ").upper()

        if column not in map(chr, range(65, 65 + COLS)):
            print("Invalid column. Please try again.")
            continue

        column_index = ord(column) - 65

        if place_checker(board, column_index, current_checker):
            if check_win(board):
                print_board(board)
                print(f"Player {current_checker} won!")
                break
            if check_draw(board):
                print_board(board)
                print("The game is a draw!")
                break
            current_player_index = (current_player_index + 1) % len(PLAYERS)  # Next player's turn
        else:
            print("Column is full. Please try again.")

if __name__ == "__main__":
    connect_4()
