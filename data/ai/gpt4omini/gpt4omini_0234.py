import os
import random

# Constants for board dimensions and player symbols
ROWS = 6
COLS = 7
PLAYERS = ["X", "O", "V", "H", "M"]  # Up to 5 players

# Function to create and initialize the game board
def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

# Function to print the game board
def print_board(board):
    os.system('clear')  # Clears the terminal screen
    print("  " + "   ".join(chr(i + 65) for i in range(COLS)))  # Column labels A, B, C, ...
    print("+" + "---+" * COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)

# Function to check if a given player has won
def check_win(board, player):
    # Horizontal check
    for r in range(ROWS):
        for c in range(COLS - 3):
            if all(board[r][c + i] == player for i in range(4)):
                return True
    # Vertical check
    for c in range(COLS):
        for r in range(ROWS - 3):
            if all(board[r + i][c] == player for i in range(4)):
                return True
    # Diagonal checks
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if all(board[r + i][c + i] == player for i in range(4)):
                return True
            if all(board[r + 3 - i][c + i] == player for i in range(4)):
                return True
    return False

# Function to check for a draw
def check_draw(board):
    return all(cell != " " for row in board for cell in row)

# Function to place a checker on the board
def place_checker(board, column, player):
    for row in reversed(board):
        if row[column] == " ":
            row[column] = player
            return True
    return False  # The column is full

# Function to get a valid column input from the player
def get_column_input(player):
    while True:
        column_input = input(f"Player {player}, please enter a column (A-G): ").upper()
        if len(column_input) == 1 and 'A' <= column_input <= 'G':
            column_index = ord(column_input) - 65  # Convert letter to column index
            return column_index  # Return the column index (0 to 6)
        print("Invalid input. Please enter a letter from A to G.")

# Main function to execute the Connect 4 game
def play_game():
    board = create_board()
    current_player = random.choice(PLAYERS)
    game_over = False

    print_board(board)

    while not game_over:
        column = get_column_input(current_player)

        if place_checker(board, column, current_player):
            print_board(board)  # Print the board after placing checker

            if check_win(board, current_player):
                print(f"Player {current_player} won!")
                game_over = True
            elif check_draw(board):
                print("The game is a draw!")
                game_over = True
            
            # Move to the next player
            current_index = PLAYERS.index(current_player)
            current_player = PLAYERS[(current_index + 1) % len(PLAYERS)]
        else:
            print(f"Column {chr(column + 65)} is full. Try another column.")

# Run the game
if __name__ == "__main__":
    play_game()
