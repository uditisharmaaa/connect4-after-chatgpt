import os
import random

# Constants for board configuration and players
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"][:PLAYERS]

def create_board(rows, cols):
    """Create an empty game board."""
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Print the current board state."""
    os.system('clear')  # Clear terminal for a better visual
    print("  " + "   ".join(chr(65 + i) for i in range(len(board[0]))))
    print("+---" * len(board[0]) + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * len(board[0]) + "+")

def is_valid_column(column, board):
    """Check if a column is a valid choice (exists and not full)."""
    return 0 <= column < len(board[0]) and board[0][column] == " "

def drop_checker(board, column, checker):
    """Drop the checker into the specified column."""
    for row in range(len(board) - 1, -1, -1):
        if board[row][column] == " ":
            board[row][column] = checker
            return row

def check_winner(board, checker):
    """Check if the given checker has won the game."""
    rows, cols = len(board), len(board[0])
    
    # Check horizontal
    for r in range(rows):
        for c in range(cols - 3):
            if all(board[r][c + i] == checker for i in range(4)):
                return True

    # Check vertical
    for c in range(cols):
        for r in range(rows - 3):
            if all(board[r + i][c] == checker for i in range(4)):
                return True

    # Check diagonal (top-left to bottom-right)
    for r in range(rows - 3):
        for c in range(cols - 3):
            if all(board[r + i][c + i] == checker for i in range(4)):
                return True

    # Check diagonal (top-right to bottom-left)
    for r in range(rows - 3):
        for c in range(3, cols):
            if all(board[r + i][c - i] == checker for i in range(4)):
                return True

    return False

def is_draw(board):
    """Check if the game is a draw (board is full)."""
    return all(board[0][c] != " " for c in range(len(board[0])))

def get_column():
    """Prompt the user for a valid column input."""
    while True:
        col = input("Please enter a column: ").strip().upper()
        if len(col) == 1 and col.isalpha():
            return ord(col) - 65
        print("Invalid input. Try again.")

def connect4():
    """Main function to play the Connect 4 game."""
    board = create_board(ROWS, COLS)
    current_player = random.randint(0, PLAYERS - 1)  # Randomly select the first player
    
    print("Welcome to Connect 4!")
    print("Players:", ", ".join(CHECKERS[:PLAYERS]))
    input("Press Enter to start...")

    while True:
        print_board(board)
        checker = CHECKERS[current_player]
        print(f"Player {checker}, it's your turn.")

        column = get_column()
        # Validate column choice
        while not is_valid_column(column, board):
            print("Invalid column. Try again.")
            column = get_column()

        # Place checker and check for win/draw
        drop_checker(board, column, checker)
        if check_winner(board, checker):
            print_board(board)
            print(f"Player {checker} won!")
            break
        if is_draw(board):
            print_board(board)
            print("The game is a draw!")
            break

        # Switch players
        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    connect4()
