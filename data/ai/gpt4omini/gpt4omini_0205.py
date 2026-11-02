import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O', 'V', 'H', 'M']

# Initialize the board
def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

# Print the board
def print_board(board):
    os.system('clear')
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))  # Column labels A-G
    print("+---" + "+---" * (COLS - 1) + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" + "+---" * (COLS - 1) + "+")

# Check for winning conditions
def check_win(board, player):
    # Check horizontal, vertical, and diagonal wins
    for r in range(ROWS):
        for c in range(COLS - 3):
            if all(board[r][c + i] == player for i in range(4)):
                return True
    for c in range(COLS):
        for r in range(ROWS - 3):
            if all(board[r + i][c] == player for i in range(4)):
                return True
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if all(board[r + i][c + i] == player for i in range(4)):
                return True
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if all(board[r - i][c + i] == player for i in range(4)):
                return True
    return False

# Check for a draw
def check_draw(board):
    return all(board[0][c] != ' ' for c in range(COLS))

# Place checker
def place_checker(board, col, player):
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == ' ':
            board[r][col] = player
            return True
    return False

# Main game loop
def play_game():
    board = create_board()
    current_player = random.choice(PLAYERS)

    while True:
        print_board(board)
        col_input = input(f"Player {current_player}, please enter a column (A-G): ").strip().upper()

        if col_input in map(chr, range(65, 65 + COLS)):  # Check for valid column
            col = ord(col_input) - 65
            if place_checker(board, col, current_player):
                if check_win(board, current_player):
                    print_board(board)
                    print(f"Player {current_player} won!")
                    break
                if check_draw(board):
                    print_board(board)
                    print("It's a draw!")
                    break
                current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % len(PLAYERS)]
            else:
                print("Column is full, try another!")
        else:
            print("Invalid input, please choose a column A-G.")

if __name__ == "__main__":
    play_game()
