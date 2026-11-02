import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
COLUMN_LABELS = [chr(ord('A') + i) for i in range(COLUMNS)]

# Initialize board
def create_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

# Print the board
def print_board(board):
    os.system('clear')  # Clears the screen
    print("  " + "   ".join(COLUMN_LABELS))
    print("+---" * COLUMNS + "+")
    for row in board:
        row_repr = "| " + " | ".join(row) + " |"
        print(row_repr)
        print("+---" * COLUMNS + "+")

# Validate user input for column choice
def get_column_choice():
    while True:
        column = input("Please enter a column: ").strip().upper()
        if column in COLUMN_LABELS:
            return COLUMN_LABELS.index(column)
        else:
            print("Invalid input. Choose a valid column (A-G).")

# Place the checker in the chosen column
def place_checker(board, column, checker):
    for row in range(ROWS - 1, -1, -1):  # Start from the bottom row
        if board[row][column] == " ":
            board[row][column] = checker
            return row, column
    return None  # Column is full

# Check for win condition
def check_winner(board, checker):
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True
    # Check vertical
    for row in range(ROWS - 3):
        for col in range(COLUMNS):
            if all(board[row + i][col] == checker for i in range(4)):
                return True
    # Check diagonal (/)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True
    # Check diagonal (\)
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True
    return False

# Check for a draw (no empty spaces)
def check_draw(board):
    return all(cell != " " for row in board for cell in row)

# Main game logic
def main():
    # Initialize game
    board = create_board()
    players = CHECKERS[:PLAYERS]
    random.shuffle(players)  # Shuffle players to select initial order
    turn = 0  # Keeps track of whose turn it is
    
    print_board(board)
    print(f"Player {players[turn]} goes first!")

    while True:
        print(f"Player {players[turn]}'s turn:")
        column = get_column_choice()
        position = place_checker(board, column, players[turn])

        if position is None:
            print(f"Column {COLUMN_LABELS[column]} is full! Choose another.")
            continue

        print_board(board)

        row, col = position
        # Check for win
        if check_winner(board, players[turn]):
            print(f"Player {players[turn]} won!")
            break

        # Check for draw
        if check_draw(board):
            print("The game is a draw!")
            break

        # Pass turn to the next player
        turn = (turn + 1) % PLAYERS

if __name__ == "__main__":
    main()
