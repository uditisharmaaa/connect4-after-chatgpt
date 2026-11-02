import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = ["X", "O", "V", "H", "M"]

# Initialize the board
def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

# Print the board
def print_board(board):
    os.system('clear')  # Clear the console (works on Linux/Unix)
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))  # Column headers from A to G
    print("+" + "---+" * COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)

# Check for valid input
def is_valid_input(user_input):
    if len(user_input) != 1 or not user_input.isalpha():
        return False
    column_index = ord(user_input.upper()) - 65  # Convert A-G to 0-6
    return 0 <= column_index < COLS

# Place the checker on the board
def place_checker(board, column, checker):
    for row in reversed(board):
        if row[column] == " ":
            row[column] = checker
            return True
    return False  # Column is full

# Check for a win condition
def check_win(board, checker):
    # Check horizontal
    for row in board:
        for col in range(COLS - 3):
            if all(cell == checker for cell in row[col:col + 4]):
                return True
    # Check vertical
    for col in range(COLS):
        for row in range(ROWS - 3):
            if all(board[row + offset][col] == checker for offset in range(4)):
                return True
    # Check diagonal (/)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - offset][col + offset] == checker for offset in range(4)):
                return True
    # Check diagonal (\)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + offset][col + offset] == checker for offset in range(4)):
                return True
    return False

# Check for a draw
def check_draw(board):
    return all(cell != " " for row in board for cell in row)

# Main game function
def play_game():
    board = create_board()
    current_player_index = random.randint(0, len(PLAYERS) - 1)
    turn_count = 0

    while True:
        print_board(board)
        current_player = PLAYERS[current_player_index]
        print(f"Player {current_player}, please enter a column (A-G): ")

        user_input = input().upper()
        
        while not is_valid_input(user_input):
            print("Invalid input. Please enter a letter from A to G:")
            user_input = input().upper()
        
        column = ord(user_input) - 65  # Convert A-G to index
        
        if not place_checker(board, column, current_player):
            print("Column full, try another column.")
            continue
        
        turn_count += 1

        if check_win(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break
        elif check_draw(board):
            print_board(board)
            print("The game is a draw!")
            break
        
        # Switch players
        current_player_index = (current_player_index + 1) % len(PLAYERS)

if __name__ == "__main__":
    play_game()
