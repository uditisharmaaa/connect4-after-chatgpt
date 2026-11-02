import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O']  # You can change this to ['X', 'O', 'V', 'H', 'M'] for more players

# Initialize the board
def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

# Print the board
def print_board(board):
    os.system('clear')  # Clear screen (Linux/Unix)
    print("  " + "   ".join(chr(i) for i in range(65, 65 + COLS)))  # Columns A-G
    print("+" + "---+" * COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)

# Check for valid input
def is_valid_input(col):
    return col in range(COLS)

# Place the checker in the board
def place_checker(board, col, checker):
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = checker
            return True
    return False  # Column is full

# Check for a win
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

    # Check diagonal (/)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True

    # Check diagonal (\)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True

    return False

# Check for a draw
def is_draw(board):
    return all(cell != ' ' for row in board for cell in row)

# Main game loop
def play_game():
    board = create_board()
    current_player = random.choice(PLAYERS)  # Randomly select the first player
    game_over = False

    print_board(board)

    while not game_over:
        col_input = input(f"Player {current_player}, please enter a column (A-G): ").upper()
        
        if len(col_input) != 1 or not col_input.isalpha():
            print("Invalid input! Please enter a letter A-G.")
            continue
        
        col = ord(col_input) - 65  # Convert letter A-G to index 0-6

        if not is_valid_input(col):
            print("Invalid column! Please enter a letter A-G.")
            continue

        if not place_checker(board, col, current_player):
            print("Column is full! Please choose another column.")
            continue
        
        print_board(board)

        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            game_over = True
            break

        if is_draw(board):
            print("The game is a draw!")
            game_over = True
            break
        
        # Switch to next player
        current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % len(PLAYERS)]

if __name__ == "__main__":
    play_game()
