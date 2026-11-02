import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = ['X', 'O', 'V', 'H', 'M']  # Up to 5 players

# Initialize the game board
def create_board():
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

# Print the game board
def print_board(board):
    os.system('clear')  # Clear the terminal screen
    print("  " + "   ".join(chr(65 + i) for i in range(COLUMNS)))  # Column headers
    print("+" + "---+" * COLUMNS)  # Top border
    for row in board:
        print("| " + " | ".join(row) + " |")  # Row contents
        print("+" + "---+" * COLUMNS)  # Row border

# Check for valid input
def is_valid_input(col_input):
    if len(col_input) == 1 and col_input.isalpha():
        col_index = ord(col_input.upper()) - 65
        return 0 <= col_index < COLUMNS
    return False

# Place a checker in the specified column
def place_checker(board, col, player):
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = player
            return True
    return False

# Check for a win condition
def check_winner(board, player):
    for r in range(ROWS):
        for c in range(COLUMNS):
            if board[r][c] == player:
                # Check horizontal
                if c + 3 < COLUMNS and all(board[r][c+i] == player for i in range(4)):
                    return True
                # Check vertical
                if r + 3 < ROWS and all(board[r+i][c] == player for i in range(4)):
                    return True
                # Check diagonals
                if r + 3 < ROWS and c + 3 < COLUMNS and all(board[r+i][c+i] == player for i in range(4)):
                    return True
                if r - 3 >= 0 and c + 3 < COLUMNS and all(board[r-i][c+i] == player for i in range(4)):
                    return True
    return False

# Check for a draw condition
def check_draw(board):
    return all(board[0][c] != ' ' for c in range(COLUMNS))

# Main game loop
def main():
    board = create_board()
    current_player_index = random.randint(0, len(PLAYERS) - 1)
    print_board(board)

    while True:
        current_player = PLAYERS[current_player_index]
        col_input = input(f"Player {current_player}, please enter a column (A-G): ").upper()

        if not is_valid_input(col_input):
            print("Invalid input. Please try again.")
            continue

        col_index = ord(col_input) - 65

        if place_checker(board, col_index, current_player):
            print_board(board)

            if check_winner(board, current_player):
                print(f"Player {current_player} won!")
                break
            if check_draw(board):
                print("The game is a draw!")
                break

            current_player_index = (current_player_index + 1) % len(PLAYERS)  # Switch to next player
        else:
            print("Column is full. Please choose another column.")

if __name__ == "__main__":
    main()
