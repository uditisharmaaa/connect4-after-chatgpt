import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O', 'V', 'H', 'M']

# Initialize the board
def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

# Print the board
def print_board(board):
    os.system('clear')  # Clear the terminal
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))  # Column labels A-G
    print("+" + "---+".join([""] * COLS) + "+")  # Top border
    for row in board:
        print("| " + " | ".join(row) + " |")  # Print each row
        print("+" + "---+".join([""] * COLS) + "+")  # Row border

# Check for a win
def check_win(board, player):
    # Check horizontal, vertical, and diagonal
    for r in range(ROWS):
        for c in range(COLS - 3):
            if all(board[r][c + i] == player for i in range(4)):
                return True
    for c in range(COLS):
        for r in range(ROWS - 3):
            if all(board[r + i][c] == player for i in range(4)):
                return True
    for c in range(COLS - 3):
        for r in range(ROWS - 3):
            if all(board[r + i][c + i] == player for i in range(4)):
                return True
    for c in range(COLS - 3):
        for r in range(3, ROWS):
            if all(board[r - i][c + i] == player for i in range(4)):
                return True
    return False

# Check for a draw
def check_draw(board):
    return all(cell != " " for row in board for cell in row)

# Place a checker
def place_checker(board, column, player):
    for r in range(ROWS - 1, -1, -1):
        if board[r][column] == " ":
            board[r][column] = player
            return True
    return False

# Main game loop
def main():
    board = create_board()
    current_player = random.choice(PLAYERS)
    print_board(board)
    
    while True:
        column = input(f"Player {current_player}, please enter a column (A-G): ").upper()
        
        if column < 'A' or column >= chr(65 + COLS):
            print("Invalid input. Please choose a column between A and G.")
            continue
        
        col_index = ord(column) - 65

        if not place_checker(board, col_index, current_player):
            print("Column is full, turn lost.")
        else:
            print_board(board)
            if check_win(board, current_player):
                print(f"Player {current_player} won!")
                break
            if check_draw(board):
                print("The game is a draw!")
                break
            
            # Switch players
            current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % len(PLAYERS)]

if __name__ == "__main__":
    main()
