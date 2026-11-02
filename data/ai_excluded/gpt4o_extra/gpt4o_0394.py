import random
import os

# Constants for the game
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

# Initialize an empty board
def create_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

# Print the current board
def print_board(board):
    os.system('clear')  # Clear the screen
    print("  " + "   ".join([chr(ord('A') + i) for i in range(COLUMNS)]))
    print("+---" * COLUMNS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

# Check if the current column selection is valid
def is_valid_selection(column, board):
    if column < 0 or column >= COLUMNS:
        return False
    if board[0][column] != " ":
        return False
    return True

# Drop the checker in the selected column
def drop_checker(board, column, checker):
    for row in reversed(board):
        if row[column] == " ":
            row[column] = checker
            break

# Check for a win condition
def check_for_win(board, checker):
    # Check horizontal win
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col+i] == checker for i in range(4)):
                return True
    # Check vertical win
    for row in range(ROWS - 3):
        for col in range(COLUMNS):
            if all(board[row+i][col] == checker for i in range(4)):
                return True
    # Check diagonal win (bottom left to top right)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row+i][col+i] == checker for i in range(4)):
                return True
    # Check diagonal win (top left to bottom right)
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row-i][col+i] == checker for i in range(4)):
                return True
    return False

# Check for a draw condition
def check_for_draw(board):
    return all(board[0][col] != " " for col in range(COLUMNS))

# Main game function
def main():
    board = create_board()
    
    # Select random starting player
    current_turn = random.randint(0, PLAYERS - 1)

    while True:
        print_board(board)
        print(f"Player {CHECKERS[current_turn]}, please enter a column:")

        # Get valid column selection
        while True:
            try:
                column = input().strip().upper()
                column_index = ord(column) - ord('A')
                if is_valid_selection(column_index, board):
                    break
                else:
                    print("Invalid selection. Try again.")
            except (IndexError, ValueError):
                print("Invalid input. Enter a valid column letter.")

        # Drop the checker in the selected column
        drop_checker(board, column_index, CHECKERS[current_turn])

        # Check for a win
        if check_for_win(board, CHECKERS[current_turn]):
            print_board(board)
            print(f"Player {CHECKERS[current_turn]} won!")
            break

        # Check for a draw
        if check_for_draw(board):
            print_board(board)
            print("The game is a draw!")
            break

        # Switch to the next player
        current_turn = (current_turn + 1) % PLAYERS

if __name__ == "__main__":
    main()
