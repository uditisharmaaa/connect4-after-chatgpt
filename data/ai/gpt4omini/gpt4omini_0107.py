import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYER_CHECKERS = ['X', 'O', 'V', 'H', 'M']

# Initialize the game board
def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

# Print the current state of the board
def print_board(board):
    os.system('clear')  # Clear the terminal screen
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))
    print("+" + "---+" * COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)

# Check for a win in all directions
def check_win(board, checker):
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True

    # Check vertical
    for col in range(COLS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == checker for i in range(4)):
                return True

    # Check diagonals (bottom-left to top-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True

    # Check diagonals (top-left to bottom-right)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True

    return False

# Check for a draw
def check_draw(board):
    return all(board[0][col] != ' ' for col in range(COLS))  # Full row

# Place the checker in the board
def place_checker(board, col, checker):
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = checker
            return True
    return False

# Main game loop
def play_game():
    board = create_board()
    players = PLAYER_CHECKERS[:2]  # Use only 2 players for the game
    current_player = random.choice(players)
    game_over = False

    print_board(board)

    while not game_over:
        valid_input = False
        while not valid_input:
            column_input = input(f"Player {current_player}, please enter a column (A-G): ").strip().upper()
            if len(column_input) == 1 and column_input >= 'A' and column_input <= chr(65 + COLS - 1):
                col = ord(column_input) - 65
                if place_checker(board, col, current_player):
                    valid_input = True
                else:
                    print("Column is full. Please choose a different column.")
            else:
                print("Invalid input. Please enter a valid column (A-G).")

        print_board(board)

        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            game_over = True
        elif check_draw(board):
            print("The game is a draw!")
            game_over = True

        current_player = players[(players.index(current_player) + 1) % len(players)]

if __name__ == "__main__":
    play_game()
