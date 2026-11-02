import os
import random

# Constants for the game
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O', 'V', 'H', 'M']

# Initialize the game board
def initialize_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

# Print the game board
def print_board(board):
    os.system('clear')  # Use 'cls' on Windows
    print("  " + "   ".join(chr(i + 65) for i in range(COLS)))  # A, B, C, ...
    print("+---" + "+---" * (COLS - 1) + "+")
    for row in range(ROWS):
        print("| " + " | ".join(board[row]) + " |")
        print("+---" + "+---" * (COLS - 1) + "+")

# Check if the column is valid and not full
def is_valid_column(board, col):
    return col >= 0 and col < COLS and board[0][col] == " "

# Place the checker in the board
def place_checker(board, col, player):
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = player
            return True
    return False

# Check for a win
def check_win(board, player):
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col + i] == player for i in range(4)):
                return True
    
    # Check vertical
    for col in range(COLS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == player for i in range(4)):
                return True
    
    # Check diagonal (positive slope)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == player for i in range(4)):
                return True

    # Check diagonal (negative slope)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i][col + i] == player for i in range(4)):
                return True
            
    return False

# Check for a draw
def check_draw(board):
    return all(board[0][col] != " " for col in range(COLS))

# Main game loop
def play_game():
    board = initialize_board()
    current_player_index = random.randint(0, len(PLAYERS) - 1)
    
    print_board(board)
    
    while True:
        current_player = PLAYERS[current_player_index]
        col_input = input(f"Player {current_player}, please enter a column (A-{chr(65 + COLS - 1)}): ").strip().upper()
        
        if col_input not in map(chr, range(65, 65 + COLS)):
            print("Invalid input. Please enter a valid column.")
            continue
        
        col = ord(col_input) - 65

        if not is_valid_column(board, col):
            print("Column full or invalid. Please select another column.")
            continue
        
        place_checker(board, col, current_player)
        print_board(board)

        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            break

        if check_draw(board):
            print("The game is a draw!")
            break

        current_player_index = (current_player_index + 1) % len(PLAYERS)

if __name__ == "__main__":
    play_game()
