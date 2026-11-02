import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]  # Maximum 5 players

# Initialize the board
def create_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]

# Print the board
def print_board(board):
    os.system('clear')  # Clear the console
    column_labels = " ".join(chr(65 + i) for i in range(len(board[0])))
    print("  " + "   ".join(column_labels))
    print(" +" + "---+" * len(board[0]))
    for row in board:
        print(" | " + " | ".join(row) + " |")
        print(" +" + "---+" * len(board[0]))

# Check if the column is valid and not full
def is_valid_column(board, column):
    if column < 0 or column >= len(board[0]):
        return False
    return board[0][column] == " "

# Place the checker in the correct location
def place_checker(board, column, checker):
    for row in range(len(board) - 1, -1, -1):
        if board[row][column] == " ":
            board[row][column] = checker
            return

# Check for a win condition
def check_win(board, checker):
    rows, cols = len(board), len(board[0])

    # Check horizontally
    for r in range(rows):
        for c in range(cols - 3):
            if all(board[r][c + i] == checker for i in range(4)):
                return True

    # Check vertically
    for c in range(cols):
        for r in range(rows - 3):
            if all(board[r + i][c] == checker for i in range(4)):
                return True

    # Check diagonally (\)
    for r in range(rows - 3):
        for c in range(cols - 3):
            if all(board[r + i][c + i] == checker for i in range(4)):
                return True

    # Check diagonally (/)
    for r in range(3, rows):
        for c in range(cols - 3):
            if all(board[r - i][c + i] == checker for i in range(4)):
                return True

    return False

# Check if the board is full (draw)
def check_draw(board):
    return all(board[0][c] != " " for c in range(len(board[0])))

# Get the column index from user input
def get_column_input(board):
    while True:
        user_input = input("Please enter a column (A-G): ").upper()
        if len(user_input) != 1 or not user_input.isalpha():
            print("Invalid input. Enter a single letter.")
            continue
        column = ord(user_input) - 65
        if not is_valid_column(board, column):
            print("Invalid column. Try again.")
            continue
        return column

# Main game loop
def connect_4():
    # Initialize the game
    board = create_board(ROWS, COLUMNS)
    players = [CHECKERS[i] for i in range(PLAYERS)]
    current_player = random.randint(0, PLAYERS - 1)
    print_board(board)

    while True:
        # Current player makes a move
        print(f"Player {players[current_player]}'s turn.")
        column = get_column_input(board)
        place_checker(board, column, players[current_player])
        print_board(board)

        # Check for win or draw
        if check_win(board, players[current_player]):
            print(f"Player {players[current_player]} won!")
            break
        if check_draw(board):
            print("It's a draw!")
            break

        # Switch to the next player
        current_player = (current_player + 1) % PLAYERS

# Run the game
if __name__ == "__main__":
    connect_4()
