import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O', 'V', 'H', 'M']  # Multiple players

# Initialize the Connect 4 board
def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

# Print the board
def print_board(board):
    os.system('clear')  # Clear the terminal screen
    print("  " + "   ".join(chr(65 + c) for c in range(COLS)))  # Column labels A-G
    print("+---+" + "---+" * (COLS - 1))
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---+" + "---+" * (COLS - 1))

# Validate player's input
def is_valid_input(player_input, board):
    if len(player_input) != 1 or not player_input.isalpha():
        return False
    col = ord(player_input.upper()) - 65
    return col >= 0 and col < COLS and board[0][col] == " "

# Place a checker in the specified column
def place_checker(board, col, player):
    for row in reversed(board):
        if row[col] == " ":
            row[col] = player
            return True
    return False

# Check for a win
def check_win(board, player):
    # Check horizontal, vertical, and diagonal positions for a win
    for r in range(ROWS):
        for c in range(COLS):
            if (
                (c + 3 < COLS and all(board[r][c+i] == player for i in range(4))) or  # Horizontal
                (r + 3 < ROWS and all(board[r+i][c] == player for i in range(4))) or  # Vertical
                (r + 3 < ROWS and c + 3 < COLS and all(board[r+i][c+i] == player for i in range(4))) or  # Diagonal right
                (r + 3 < ROWS and c - 3 >= 0 and all(board[r+i][c-i] == player for i in range(4)))  # Diagonal left
            ):
                return True
    return False

# Check for a draw
def is_draw(board):
    return all(board[0][c] != " " for c in range(COLS))

# Main function to run the Connect 4 game
def connect_4():
    board = create_board()
    current_player_index = random.randint(0, len(PLAYERS) - 1)  # Random starting player
    game_over = False

    print_board(board)

    while not game_over:
        current_player = PLAYERS[current_player_index]
        player_input = input(f"Player {current_player}, please enter a column: ")

        while not is_valid_input(player_input, board):
            player_input = input("Invalid input. Please enter a valid column: ")

        col = ord(player_input.upper()) - 65

        if not place_checker(board, col, current_player):
            print("Column is full! Try another column.")
            continue  # Player does not lose turn

        print_board(board)

        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            game_over = True
        elif is_draw(board):
            print("The game is a draw!")
            game_over = True

        # Move to the next player
        current_player_index = (current_player_index + 1) % len(PLAYERS)

# Start the game
if __name__ == "__main__":
    connect_4()
