import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = ["X", "O", "V", "H", "M"]  # Maximum 5 players

# Initialize the board
def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

# Print the board
def print_board(board):
    os.system('clear')  # Clear the screen (for Linux/Unix)
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))  # Column labels A, B, C...
    print("+" + "---+" * COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)

# Check if the column is valid for dropping
def is_valid_column(board, col):
    return board[0][col] == " "

# Drop the checker in the column
def drop_checker(board, col, checker):
    for row in reversed(board):
        if row[col] == " ":
            row[col] = checker
            return True
    return False  # Column is full

# Check for a win
def check_win(board, checker):
    # Check horizontal
    for row in board:
        for col in range(len(row) - 3):
            if all(row[col + i] == checker for i in range(4)):
                return True
    
    # Check vertical
    for col in range(COLS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == checker for i in range(4)):
                return True

    # Check diagonal (down-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True

    # Check diagonal (down-left)
    for row in range(ROWS - 3):
        for col in range(3, COLS):
            if all(board[row + i][col - i] == checker for i in range(4)):
                return True
    
    return False

# Check for a draw
def is_draw(board):
    return all(board[0][col] != " " for col in range(COLS))

# Main function to run the game
def play_game():
    board = create_board()
    current_player_index = random.randint(0, len(PLAYERS) - 1)
    print_board(board)
    
    while True:
        current_player = PLAYERS[current_player_index]
        col_input = input(f"Player {current_player}, please enter a column (A-G): ").upper()
        if col_input not in [chr(65 + i) for i in range(COLS)]:
            print("Invalid input. Please choose a column between A and G.")
            continue
        
        col = ord(col_input) - 65
        if is_valid_column(board, col):
            drop_checker(board, col, current_player)
            print_board(board)
            if check_win(board, current_player):
                print(f"Player {current_player} won!")
                break
            if is_draw(board):
                print("The game is a draw!")
                break
            
            current_player_index = (current_player_index + 1) % len(PLAYERS)  # Next player
        else:
            print("Column is full. Choose another column.")

if __name__ == "__main__":
    play_game()
