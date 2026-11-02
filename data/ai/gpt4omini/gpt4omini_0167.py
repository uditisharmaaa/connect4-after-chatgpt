import os
import random

# Constants
ROWS = 6
COLS = 7
MAX_PLAYERS = 5
PLAYERS_CHECKERS = ['X', 'O', 'V', 'H', 'M']

# Initialize the board
def initialize_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

# Print the board
def print_board(board):
    os.system('clear')  # Clear the terminal screen
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))  # Column labels A, B, C, ...
    print("+---" + "---+" * COLS)  # Top border
    for row in board:
        print("| " + " | ".join(row) + " |")  # Row contents
        print("+---" + "---+" * COLS)  # Row border

# Check if the move is valid
def is_valid_move(board, col):
    return 0 <= col < COLS and board[0][col] == " "

# Place the checker in the board
def place_checker(board, checker, col):
    for row in reversed(board):
        if row[col] == " ":
            row[col] = checker
            return True
    return False

# Check for a win
def check_win(board, checker):
    # Check horizontal
    for row in board:
        for col in range(COLS - 3):
            if all(cell == checker for cell in row[col:col + 4]):
                return True
                
    # Check vertical
    for col in range(COLS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == checker for i in range(4)):
                return True

    # Check diagonal (bottom-left to top-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True

    # Check diagonal (top-left to bottom-right)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True

    return False

# Check for a draw
def is_draw(board):
    return all(board[0][col] != " " for col in range(COLS))

# Main game function
def connect_4():
    board = initialize_board()
    players = PLAYERS_CHECKERS[:2]  # Default to 2 players
    current_player = random.choice(players)

    print_board(board)

    while True:
        print(f"Player {current_player}, please enter a column (A-G):")
        user_input = input().strip().upper()

        if len(user_input) != 1 or not user_input.isalpha():
            print("Invalid input. Please enter a letter from A to G.")
            continue
        
        col = ord(user_input) - 65  # Convert letter to column index

        if is_valid_move(board, col):
            place_checker(board, current_player, col)
            print_board(board)
            
            if check_win(board, current_player):
                print(f"Player {current_player} won!")
                break
            elif is_draw(board):
                print("The game is a draw!")
                break
            
            current_player = players[(players.index(current_player) + 1) % len(players)]
        else:
            print("Column is full or invalid. Please select another column.")

if __name__ == "__main__":
    connect_4()
