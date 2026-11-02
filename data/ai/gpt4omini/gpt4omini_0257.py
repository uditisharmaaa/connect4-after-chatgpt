import os
import random

# Constants for the game
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O']  # Allowing up to 5 players: ['X', 'O', 'V', 'H', 'M']

# Function to create an empty board
def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

# Function to print the board
def print_board(board):
    os.system('clear')  # Clear the terminal screen (Linux/Unix)
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))  # Column labels A, B, C, ...
    print("+" + "---+" * COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)

# Function to check if the current player has won the game
def check_win(board, player):
    # Check horizontal, vertical and diagonal directions
    for r in range(ROWS):
        for c in range(COLS):
            if (c <= COLS - 4 and all(board[r][c + k] == player for k in range(4))) or \
               (r <= ROWS - 4 and all(board[r + k][c] == player for k in range(4))) or \
               (r <= ROWS - 4 and c <= COLS - 4 and all(board[r + k][c + k] == player for k in range(4))) or \
               (r >= 3 and c <= COLS - 4 and all(board[r - k][c + k] == player for k in range(4))):
                return True
    return False

# Function to check for a draw
def check_draw(board):
    return all(board[0][c] != " " for c in range(COLS))

# Function to place a checker on the board
def place_checker(board, column, player):
    for r in range(ROWS - 1, -1, -1):  # Start from the bottom row
        if board[r][column] == " ":
            board[r][column] = player
            return True
    return False

# Main game function
def connect_4():
    board = create_board()
    current_player_index = random.randint(0, len(PLAYERS) - 1)
    game_over = False

    while not game_over:
        print_board(board)
        current_player = PLAYERS[current_player_index]
        valid_move = False

        while not valid_move:
            column_input = input(f"Player {current_player}, please enter a column (A-{chr(65 + COLS - 1)}): ").upper()
            if column_input in [chr(65 + i) for i in range(COLS)]:
                column = ord(column_input) - 65  # Convert letter to index
                valid_move = place_checker(board, column, current_player)
                if not valid_move:
                    print("Column is full, please choose a different column.")
            else:
                print("Invalid input. Please enter a letter corresponding to a column.")

        if check_win(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            game_over = True
        elif check_draw(board):
            print_board(board)
            print("The game is a draw!")
            game_over = True

        current_player_index = (current_player_index + 1) % len(PLAYERS)  # Move to the next player

# Run the game
if __name__ == "__main__":
    connect_4()
