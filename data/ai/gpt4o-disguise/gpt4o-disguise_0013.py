import os
import random

# Constants
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

# Create board
def create_board():
    return [[" " for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]

# Print board
def print_board(board):
    os.system('clear')
    print("  " + "   ".join(chr(65 + i) for i in range(NUM_COLS)))
    for row in board:
        print("+---" * NUM_COLS + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * NUM_COLS + "+")

# Check for win
def check_win(board, checker):
    for row in range(NUM_ROWS):
        for col in range(NUM_COLS):
            if col <= NUM_COLS - 4:
                if all(board[row][c] == checker for c in range(col, col + 4)):
                    return True
            if row <= NUM_ROWS - 4:
                if all(board[r][col] == checker for r in range(row, row + 4)):
                    return True
            if row <= NUM_ROWS - 4 and col <= NUM_COLS - 4:
                if all(board[row + i][col + i] == checker for i in range(4)):
                    return True
            if row >= 3 and col <= NUM_COLS - 4:
                if all(board[row - i][col + i] == checker for i in range(4)):
                    return True
    return False

# Check for draw
def check_draw(board):
    return all(board[0][col] != " " for col in range(NUM_COLS))

# Place checker
def place_checker(board, col, checker):
    for row in reversed(range(NUM_ROWS)):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    return False

# Get valid column input
def get_valid_column():
    while True:
        choice = input("Please enter a column: ").strip()
        if len(choice) == 1 and choice.isalpha():
            col = ord(choice.upper()) - 65
            if 0 <= col < NUM_COLS:
                return col
        print("Invalid input. Try again.")

# Main game loop
def main():
    board = create_board()
    current_player = random.randint(0, NUM_PLAYERS - 1)
    print_board(board)
    while True:
        print(f"Player {CHECKERS[current_player]}, please enter a column:")
        col = get_valid_column()
        if not place_checker(board, col, CHECKERS[current_player]):
            print("Column is full. Turn lost.")
        else:
            print_board(board)
            if check_win(board, CHECKERS[current_player]):
                print(f"Player {CHECKERS[current_player]} won!")
                break
            if check_draw(board):
                print("Game is a draw!")
                break
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
