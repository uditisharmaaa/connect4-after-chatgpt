import os
import random

# Constants for board dimensions and players
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

# Function to initialize the game board
def create_board(rows, columns):
    return [[' ' for _ in range(columns)] for _ in range(rows)]

# Function to print the board
def print_board(board, columns):
    os.system('clear')  # Clear the screen (Unix/Linux terminal)
    print("  " + "   ".join(chr(65 + i) for i in range(columns)))
    print("+" + "---+" * columns)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * columns)

# Function to check if a move is valid
def is_valid_move(board, column):
    return board[0][column] == ' '

# Function to place a checker on the board
def place_checker(board, column, checker):
    for row in reversed(board):
        if row[column] == ' ':
            row[column] = checker
            break

# Function to check for a win condition
def check_win(board, checker):
    # Horizontal
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True

    # Vertical
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == checker for i in range(4)):
                return True

    # Diagonal (bottom left to top right)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True

    # Diagonal (top left to bottom right)
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True

    return False

# Function to check for a draw
def check_draw(board):
    return all(board[0][col] != ' ' for col in range(COLUMNS))

# Function to get a valid column input from the player
def get_move(columns):
    while True:
        move = input("Please enter a column (A-G): ").strip().upper()
        if len(move) == 1 and 'A' <= move <= chr(65 + columns - 1):
            return ord(move) - 65  # Convert letter to column index
        print("Invalid input. Try again.")

# Main function to play the game
def play_game():
    board = create_board(ROWS, COLUMNS)
    print_board(board, COLUMNS)

    # Randomly select the starting player
    current_player = random.randint(0, MAX_PLAYERS - 1)
    
    while True:
        checker = CHECKERS[current_player]
        print(f"Player {checker}'s turn.")
        
        column = get_move(COLUMNS)
        if not is_valid_move(board, column):
            print("Column is full. You lose the turn.")
            current_player = (current_player + 1) % MAX_PLAYERS
            continue

        place_checker(board, column, checker)
        print_board(board, COLUMNS)

        if check_win(board, checker):
            print(f"Player {checker} won!")
            break

        if check_draw(board):
            print("The game is a draw!")
            break

        current_player = (current_player + 1) % MAX_PLAYERS

if __name__ == "__main__":
    play_game()
