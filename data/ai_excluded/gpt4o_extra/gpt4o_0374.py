import os
import random

# Constants for the board size and number of players
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
CHECKERS = ["X", "O", "V", "H", "M"]

# Function to create the board
def create_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

# Function to print the board
def print_board(board):
    os.system('clear')
    print("  " + "   ".join([chr(ord('A') + i) for i in range(COLUMNS)]))
    print("+" + "---+" * COLUMNS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLUMNS)

# Function to check for a win
def check_win(board, checker):
    # Horizontal check
    for row in board:
        for col in range(COLUMNS - 3):
            if row[col] == checker and row[col + 1] == checker and row[col + 2] == checker and row[col + 3] == checker:
                return True
                
    # Vertical check
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if board[row][col] == checker and board[row + 1][col] == checker and board[row + 2][col] == checker and board[row + 3][col] == checker:
                return True
    
    # Diagonal check (bottom-left to top-right)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if board[row][col] == checker and board[row + 1][col + 1] == checker and board[row + 2][col + 2] == checker and board[row + 3][col + 3] == checker:
                return True

    # Diagonal check (top-left to bottom-right)
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if board[row][col] == checker and board[row - 1][col + 1] == checker and board[row - 2][col + 2] == checker and board[row - 3][col + 3] == checker:
                return True

    return False

# Function to check if the board is full
def is_draw(board):
    return all(board[0][col] != " " for col in range(COLUMNS))

# Function to drop the checker into the board
def drop_checker(board, col, checker):
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    return False

# Main function to run the game
def main():
    board = create_board()
    players = 2 # Set to 2 for the assignment submission
    current_player = random.randint(0, players - 1)
    print_board(board)

    while True:
        # Get current player's checker
        checker = CHECKERS[current_player]
        col = None

        # Input loop to validate user input
        while col is None:
            try:
                col_input = input(f"Player {checker}, please enter a column: ").upper()
                if len(col_input) != 1 or not col_input.isalpha():
                    raise ValueError
                col = ord(col_input) - ord('A')
                if col < 0 or col >= COLUMNS:
                    raise ValueError
                if board[0][col] != " ":
                    print("Column is full. Try a different column.")
                    col = None
            except ValueError:
                print("Invalid input. Please enter a valid column letter.")

        # Drop the checker
        drop_checker(board, col, checker)
        print_board(board)

        # Check for win
        if check_win(board, checker):
            print(f"Player {checker} won!")
            break

        # Check for draw
        if is_draw(board):
            print("The game is a draw!")
            break

        # Switch to the next player
        current_player = (current_player + 1) % players

if __name__ == "__main__":
    main()
