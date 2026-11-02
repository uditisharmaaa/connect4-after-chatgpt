import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = ["X", "O"]

# Function to create an empty board
def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

# Function to print the board
def print_board(board):
    os.system('clear')  # Clear the console
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))  # Print column labels A-G
    print("+---" + "---+" * (COLS - 1) + "---+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" + "---+" * (COLS - 1) + "---+")

# Function to check if the move is valid
def is_valid_move(board, col):
    return 0 <= col < COLS and board[0][col] == " "

# Function to place the checker in the board
def place_checker(board, col, checker):
    for row in reversed(board):
        if row[col] == " ":
            row[col] = checker
            return True
    return False

# Function to check for a win
def check_win(board, checker):
    # Check horizontal, vertical, and diagonal wins
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == checker:
                # Check horizontally
                if c + 3 < COLS and all(board[r][c + i] == checker for i in range(4)):
                    return True
                # Check vertically
                if r + 3 < ROWS and all(board[r + i][c] == checker for i in range(4)):
                    return True
                # Check diagonal /
                if r - 3 >= 0 and c + 3 < COLS and all(board[r - i][c + i] == checker for i in range(4)):
                    return True
                # Check diagonal \
                if r + 3 < ROWS and c + 3 < COLS and all(board[r + i][c + i] == checker for i in range(4)):
                    return True
    return False

# Function to check for a draw
def check_draw(board):
    return all(board[0][c] != " " for c in range(COLS))

# Main function for the game
def main():
    board = create_board()
    current_player = random.choice(PLAYERS)
    print_board(board)

    while True:
        print(f"Player {current_player}, please enter a column (A-G):")
        move = input().strip().upper()

        # Validate input
        if len(move) != 1 or move < "A" or move >= chr(65 + COLS):
            print("Invalid input. Please enter a valid column (A-G).")
            continue

        col = ord(move) - 65  # Convert column letter to index

        if is_valid_move(board, col):
            place_checker(board, col, current_player)
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
            print("Column is full! Please choose another column.")

if __name__ == "__main__":
    main()
