import os
import random

# Constants for board dimensions and player configuration
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

# Initialize board as a 2D list filled with whitespaces
def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

# Print the current state of the board
def print_board(board):
    os.system('clear')
    column_labels = "  " + "   ".join(chr(65 + i) for i in range(len(board[0])))
    print(column_labels)
    print("+---" * len(board[0]) + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * len(board[0]) + "+")

# Validate user input
def is_valid_input(input_char, board):
    if len(input_char) != 1 or not input_char.isalpha():
        return False
    col_index = ord(input_char.upper()) - 65
    return 0 <= col_index < len(board[0]) and board[0][col_index] == " "

# Place a checker in the selected column
def place_checker(board, col_index, checker):
    for row in reversed(board):
        if row[col_index] == " ":
            row[col_index] = checker
            return

# Check for a win
def check_win(board, checker):
    rows, cols = len(board), len(board[0])

    # Horizontal check
    for row in range(rows):
        for col in range(cols - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True

    # Vertical check
    for row in range(rows - 3):
        for col in range(cols):
            if all(board[row + i][col] == checker for i in range(4)):
                return True

    # Diagonal (top-left to bottom-right)
    for row in range(rows - 3):
        for col in range(cols - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True

    # Diagonal (top-right to bottom-left)
    for row in range(rows - 3):
        for col in range(3, cols):
            if all(board[row + i][col - i] == checker for i in range(4)):
                return True

    return False

# Check if the board is filled (draw condition)
def check_draw(board):
    return all(cell != " " for row in board for cell in row)

# Main function
def main():
    # Set up game
    board = create_board(ROWS, COLS)
    players = [CHECKERS[i] for i in range(PLAYERS)]
    current_player_index = random.randint(0, PLAYERS - 1)
    
    # Print initial state of the board
    print_board(board)

    while True:
        # Get current player and their checker
        current_player = players[current_player_index]
        
        # Prompt user for input
        col_input = input(f"Player {current_player}, please enter a column: ").strip().upper()
        
        # Validate input
        if not is_valid_input(col_input, board):
            print("Invalid input. Please try again.")
            continue
        
        # Determine column index and place checker
        col_index = ord(col_input) - 65
        place_checker(board, col_index, current_player)

        # Print updated board
        print_board(board)
        
        # Check for win or draw
        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            break
        elif check_draw(board):
            print("The game is a draw!")
            break
        
        # Switch to next player
        current_player_index = (current_player_index + 1) % PLAYERS

if __name__ == "__main__":
    main()
