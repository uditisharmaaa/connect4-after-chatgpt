import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O']

# Initialize the game board
def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

# Print the game board
def print_board(board):
    os.system('clear')  # Clear the terminal
    print("  " + "   ".join(chr(65 + c) for c in range(COLS)))  # Column labels A-G
    print("+---" * COLS + "+")  # Top border
    for row in board:
        print("| " + " | ".join(row) + " |")  # Row contents
        print("+---" * COLS + "+")  # Bottom border

# Check for a win in all directions
def check_win(board, player):
    # Check horizontal, vertical and diagonal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col + i] == player for i in range(4)):
                return True
    for col in range(COLS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == player for i in range(4)):
                return True
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == player for i in range(4)):
                return True
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i][col + i] == player for i in range(4)):
                return True
    return False

# Check for draw
def check_draw(board):
    return all(board[0][col] != ' ' for col in range(COLS))

# Place the checker in the board
def place_checker(board, col, player):
    for row in reversed(range(ROWS)):
        if board[row][col] == ' ':
            board[row][col] = player
            return True
    return False

# Main game loop
def main():
    board = create_board()
    random_player_index = random.randint(0, len(PLAYERS) - 1)
    current_player_index = random_player_index

    print_board(board)

    while True:
        current_player = PLAYERS[current_player_index]
        column_input = input(f"Player {current_player}, please enter a column: ").upper()

        if len(column_input) != 1 or not column_input.isalpha() or ord(column_input) < 65 or ord(column_input) >= 65 + COLS:
            print("Invalid input. Please enter a valid column (A-G).")
            continue
        
        col = ord(column_input) - 65  # Convert to column index

        if place_checker(board, col, current_player):
            print_board(board)

            if check_win(board, current_player):
                print(f"Player {current_player} won!")
                break
            
            if check_draw(board):
                print("The game is a draw!")
                break
            
            # Switch to the next player
            current_player_index = (current_player_index + 1) % len(PLAYERS)
        else:
            print("Column is full. Please choose another column.")

if __name__ == "__main__":
    main()
