import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = ['X', 'O']  # For 2 player game

# Create and initialize the board
def create_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

# Print the current state of the board
def print_board(board):
    os.system('clear')  # Clear the screen
    print("  " + "   ".join(chr(65 + i) for i in range(COLUMNS)))  # Column labels A to G
    print("+" + "---+" * COLUMNS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLUMNS)

# Check if a move is valid
def is_valid_move(board, col):
    if 0 <= col < COLUMNS and board[0][col] == " ":
        return True
    return False

# Place a checker in the board
def place_checker(board, col, checker):
    for row in reversed(range(ROWS)):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    return False

# Check for a win
def check_win(board, checker):
    # Check horizontal, vertical, and diagonal conditions for a win
    for row in range(ROWS):
        for col in range(COLUMNS):
            if (col + 3 < COLUMNS and all(board[row][col + i] == checker for i in range(4))) or \
               (row + 3 < ROWS and all(board[row + i][col] == checker for i in range(4))) or \
               (row + 3 < ROWS and col + 3 < COLUMNS and all(board[row + i][col + i] == checker for i in range(4))) or \
               (row >= 3 and col + 3 < COLUMNS and all(board[row - i][col + i] == checker for i in range(4))):
                return True
    return False

# Check if the board is full
def is_draw(board):
    for row in board:
        if " " in row:
            return False
    return True

# Main game function
def play_game():
    board = create_board()
    current_player = random.choice(PLAYERS)
    game_over = False

    while not game_over:
        print_board(board)
        print(f"Player {current_player}, please enter a column (A-G): ")
        
        col_input = input().upper()
        if len(col_input) != 1 or col_input < 'A' or col_input >= chr(65 + COLUMNS):
            print("Invalid input. Please enter a letter from A to G.")
            continue
        
        col = ord(col_input) - 65
        
        if not is_valid_move(board, col):
            print("Column is full or invalid. Try again.")
            continue
        
        place_checker(board, col, current_player)

        if check_win(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            game_over = True
        elif is_draw(board):
            print_board(board)
            print("The game is a draw!")
            game_over = True
        
        # Switch player
        current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % len(PLAYERS)]
    
if __name__ == "__main__":
    play_game()
