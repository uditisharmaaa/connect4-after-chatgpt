import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O', 'V', 'H', 'M']  # Up to 5 players

# Function to initialize the board
def initialize_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

# Function to print the current state of the board
def print_board(board):
    os.system('clear')  # Clear the terminal screen
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))
    print("+---+" + "---+" * (COLS - 1))
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---+" + "---+" * (COLS - 1))

# Function to place the checker in the appropriate position
def place_checker(board, column, player):
    for row in reversed(board):  # Start from the bottom row
        if row[column] == " ":
            row[column] = player
            return True
    return False  # Column is full

# Function to check for a win
def check_win(board, player):
    # Check horizontal, vertical, and diagonal
    for r in range(ROWS):
        for c in range(COLS):
            if (c <= COLS - 4 and
                all(board[r][c + i] == player for i in range(4))):
                return True
            if (r <= ROWS - 4 and
                all(board[r + i][c] == player for i in range(4))):
                return True
            if (r <= ROWS - 4 and c <= COLS - 4 and
                all(board[r + i][c + i] == player for i in range(4))):
                return True
            if (r >= 3 and c <= COLS - 4 and
                all(board[r - i][c + i] == player for i in range(4))):
                return True
    return False

# Function to check if the board is full (draw condition)
def check_draw(board):
    return all(board[0][c] != " " for c in range(COLS))

# Main game function
def play_game():
    board = initialize_board()
    current_player_index = random.randint(0, len(PLAYERS) - 1)
    players_count = 2  # Set for 2 players
    players = PLAYERS[:players_count]  # Select players
    print_board(board)

    while True:
        current_player = players[current_player_index]
        valid_input = False

        while not valid_input:
            try:
                col_input = input(f"Player {current_player}, please enter a column (A-G): ").upper()
                column = ord(col_input) - 65  # Convert letter to column index

                if column < 0 or column >= COLS:
                    print("Invalid column. Please choose a letter between A and G.")
                    continue
                if place_checker(board, column, current_player):
                    valid_input = True
                else:
                    print("Column is full. Choose another column.")
            except (ValueError, IndexError):
                print("Invalid input. Please enter a valid column letter (A-G).")

        print_board(board)

        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            break
        if check_draw(board):
            print("The game is a draw!")
            break

        current_player_index = (current_player_index + 1) % players_count

if __name__ == "__main__":
    play_game()
