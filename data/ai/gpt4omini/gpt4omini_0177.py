import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O']  # Extend this for more players

# Initialize the board
def initialize_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

# Print the board
def print_board(board):
    os.system('clear')  # Clear the screen
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))  # Column labels A, B, C, ...
    print("+" + "---+" * COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)

# Check for valid input
def is_valid_input(col, board):
    if col < 0 or col >= COLS:
        return False
    return board[0][col] == " "  # Check if the column is not full

# Place the checker in the column
def place_checker(col, player, board):
    for row in reversed(range(ROWS)):
        if board[row][col] == " ":
            board[row][col] = player
            return True
    return False

# Check for a win
def check_win(board, player):
    # Check horizontal
    for r in range(ROWS):
        for c in range(COLS - 3):
            if all(board[r][c + i] == player for i in range(4)):
                return True

    # Check vertical
    for r in range(ROWS - 3):
        for c in range(COLS):
            if all(board[r + i][c] == player for i in range(4)):
                return True

    # Check diagonal /
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if all(board[r - i][c + i] == player for i in range(4)):
                return True

    # Check diagonal \
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if all(board[r + i][c + i] == player for i in range(4)):
                return True

    return False

# Check for a draw
def is_draw(board):
    return all(board[0][col] != " " for col in range(COLS))

# Main game loop
def play_game():
    board = initialize_board()
    current_player = random.choice(PLAYERS)  # Randomly select the first player

    while True:
        print_board(board)
        col_input = input(f"Player {current_player}, please enter a column (A-G): ").upper()
        
        if len(col_input) == 1 and col_input in "ABCDEFG":
            col = ord(col_input) - 65  # Convert column letter to index

            if is_valid_input(col, board):
                place_checker(col, current_player, board)

                if check_win(board, current_player):
                    print_board(board)
                    print(f"Player {current_player} won!")
                    break

                if is_draw(board):
                    print_board(board)
                    print("It's a draw!")
                    break

                # Switch player
                current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % len(PLAYERS)]
            else:
                print("Column is full. Try again.")
        else:
            print("Invalid input. Please choose a column between A and G.")

if __name__ == "__main__":
    play_game()
