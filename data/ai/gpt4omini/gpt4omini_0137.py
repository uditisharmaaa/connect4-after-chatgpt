import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = ["X", "O"]  # Up to 5 players could be added if needed

# Initialize empty board
def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

# Function to print the board
def print_board(board):
    os.system('clear')  # Clear screen
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))  # Column labels A, B, C, ...
    print("+" + "---+" * COLS)  # Top border
    for row in board:
        print("|" + "|".join(f" {cell} " for cell in row) + "|")  # Rows
        print("+" + "---+" * COLS)  # Row border

# Function to check if the move is valid
def is_valid_move(board, column):
    return 0 <= column < COLS and board[0][column] == " "

# Function to place a checker in the board
def place_checker(board, column, checker):
    for row in reversed(board):
        if row[column] == " ":
            row[column] = checker
            return

# Function to check for a win (horizontal, vertical, diagonal)
def check_win(board, checker):
    # Check horizontal
    for row in board:
        for col in range(COLS - 3):
            if all(cell == checker for cell in row[col:col + 4]):
                return True
                
    # Check vertical
    for col in range(COLS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == checker for i in range(4)):
                return True
                
    # Check diagonal (positive slope)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True

    # Check diagonal (negative slope)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True
    
    return False

# Function to check for a draw
def check_draw(board):
    return all(cell != " " for row in board for cell in row)

# Main game loop
def main():
    board = create_board()
    current_player = random.choice(PLAYERS)
    
    print_board(board)

    while True:
        col_input = input(f"Player {current_player}, please enter a column (A-G): ").upper()
        
        if col_input in [chr(65 + i) for i in range(COLS)]:
            column = ord(col_input) - 65
            
            if is_valid_move(board, column):
                place_checker(board, column, current_player)
                print_board(board)

                if check_win(board, current_player):
                    print(f"Player {current_player} won!")
                    break

                if check_draw(board):
                    print("The game is a draw!")
                    break

                # Switch player
                current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % len(PLAYERS)]
            else:
                print("Column is full! Try again.")
        else:
            print("Invalid input! Please enter a letter from A to G.")

if __name__ == "__main__":
    main()
