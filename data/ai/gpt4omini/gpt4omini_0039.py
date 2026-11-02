import os
import random

# Constants for the game
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O', 'V', 'H', 'M']  # Up to 5 players

# Initialize the game board
def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

# Print the game board
def print_board(board):
    os.system('clear')  # Clear the screen before printing
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))  # Column labels A, B, C, ...
    print("+---+" + "---+" * (COLS - 1) + "---+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---+" + "---+" * (COLS - 1) + "---+")

# Validate user's input
def is_valid_input(column):
    if len(column) != 1:
        return False
    if column not in [chr(65 + i) for i in range(COLS)]:
        return False
    return True

# Place the checker in the board
def place_checker(board, col, checker):
    for row in reversed(board):
        if row[col] == " ":
            row[col] = checker
            return True
    return False

# Check for a win condition
def check_winner(board, checker):
    # Check horizontal
    for r in range(ROWS):
        for c in range(COLS - 3):
            if all(board[r][c + i] == checker for i in range(4)):
                return True

    # Check vertical
    for r in range(ROWS - 3):
        for c in range(COLS):
            if all(board[r + i][c] == checker for i in range(4)):
                return True

    # Check diagonal (bottom-left to top-right)
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if all(board[r + i][c + i] == checker for i in range(4)):
                return True

    # Check diagonal (top-left to bottom-right)
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if all(board[r - i][c + i] == checker for i in range(4)):
                return True

    return False

# Check for a draw
def check_draw(board):
    return all(board[0][c] != " " for c in range(COLS))

# Main Connect 4 game function
def play_game():
    board = create_board()
    current_player_index = random.randint(0, len(PLAYERS) - 1)
    num_players = len(PLAYERS)

    while True:
        print_board(board)
        current_player = PLAYERS[current_player_index]
        column = input(f"Player {current_player}, please enter a column: ").upper()

        while not is_valid_input(column):
            print("Invalid input. Please enter a valid column (A-G).")
            column = input(f"Player {current_player}, please enter a column: ").upper()

        col_index = ord(column) - 65  # Convert letter to column index
        
        if not place_checker(board, col_index, current_player):
            print("Column is full. You lose your turn.")
        else:
            if check_winner(board, current_player):
                print_board(board)
                print(f"Player {current_player} won!")
                break

            if check_draw(board):
                print_board(board)
                print("The game is a draw!")
                break

            current_player_index = (current_player_index + 1) % num_players  # Switch player

if __name__ == "__main__":
    play_game()
