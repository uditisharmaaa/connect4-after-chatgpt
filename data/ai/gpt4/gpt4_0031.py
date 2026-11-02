import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
CHECKERS = ["X", "O", "V", "H", "M"]

# Initialize the board
def initialize_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]

# Print the board
def print_board(board):
    os.system('clear')  # Clear the screen
    column_labels = "  ".join(chr(65 + i) for i in range(len(board[0])))
    print("  " + column_labels)
    print("+" + "---+" * len(board[0]))
    for row in board:
        print("|" + "|".join(f" {cell} " for cell in row) + "|")
        print("+" + "---+" * len(board[0]))

# Drop a checker in the specified column
def drop_checker(board, column, checker):
    for row in reversed(board):
        if row[column] == " ":
            row[column] = checker
            return True
    return False

# Check for a win
def check_winner(board, checker):
    rows, cols = len(board), len(board[0])

    # Check horizontal
    for r in range(rows):
        for c in range(cols - 3):
            if all(board[r][c + i] == checker for i in range(4)):
                return True

    # Check vertical
    for r in range(rows - 3):
        for c in range(cols):
            if all(board[r + i][c] == checker for i in range(4)):
                return True

    # Check major diagonal
    for r in range(rows - 3):
        for c in range(cols - 3):
            if all(board[r + i][c + i] == checker for i in range(4)):
                return True

    # Check minor diagonal
    for r in range(3, rows):
        for c in range(cols - 3):
            if all(board[r - i][c + i] == checker for i in range(4)):
                return True

    return False

# Check for a draw
def check_draw(board):
    return all(cell != " " for row in board for cell in row)

# Validate user input
def get_valid_column_input(board, num_columns):
    while True:
        user_input = input("Please enter a column: ").strip().upper()
        if len(user_input) != 1 or not ("A" <= user_input < chr(65 + num_columns)):
            print("Invalid column. Please try again.")
            continue
        column = ord(user_input) - 65
        if board[0][column] != " ":
            print("Column is full. Please try again.")
            continue
        return column

# Main game logic
def main():
    # Set up game parameters
    board = initialize_board(ROWS, COLUMNS)
    num_players = 2
    players = CHECKERS[:num_players]
    random.shuffle(players)
    
    current_player_idx = 0

    # Game loop
    print_board(board)
    while True:
        current_player = players[current_player_idx]
        print(f"Player {current_player}'s turn.")
        column = get_valid_column_input(board, COLUMNS)
        drop_checker(board, column, current_player)
        
        print_board(board)

        # Check for a win
        if check_winner(board, current_player):
            print(f"Player {current_player} won!")
            break

        # Check for a draw
        if check_draw(board):
            print("The game is a draw!")
            break

        # Switch to next player
        current_player_idx = (current_player_idx + 1) % num_players

if __name__ == "__main__":
    main()
