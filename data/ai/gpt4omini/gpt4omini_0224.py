import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O', 'V', 'H', 'M']  # Up to 5 players

# Create the board
def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

# Print the board
def print_board(board):
    os.system('clear')
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))  # Column labels (A-G)
    print("+" + "---+" * COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)

# Check for a win
def check_win(board, player):
    # Check horizontal, vertical, and diagonal
    for r in range(ROWS):
        for c in range(COLS):
            if (c + 3 < COLS and all(board[r][c + i] == player for i in range(4))) or \
               (r + 3 < ROWS and all(board[r + i][c] == player for i in range(4))) or \
               (r + 3 < ROWS and c + 3 < COLS and all(board[r + i][c + i] == player for i in range(4))) or \
               (r + 3 < ROWS and c - 3 >= 0 and all(board[r + i][c - i] == player for i in range(4))):
                return True
    return False

# Check for a draw
def check_draw(board):
    return all(board[0][c] != " " for c in range(COLS))

# Place a checker in the board
def place_checker(board, column, player):
    for row in range(ROWS - 1, -1, -1):  # Start from the bottom
        if board[row][column] == " ":
            board[row][column] = player
            return True
    return False

# Main game function
def play_game():
    board = create_board()
    current_player_index = random.randint(0, 1)  # Random initial player for 2 players
    print_board(board)

    while True:
        current_player = PLAYERS[current_player_index]
        valid_move = False

        while not valid_move:
            column_input = input(f"Player {current_player}, please enter a column (A-G): ").upper()
            if len(column_input) != 1 or column_input < 'A' or column_input > chr(64 + COLS):
                print("Invalid input. Please enter a letter between A and G.")
                continue

            column = ord(column_input) - 65  # Convert letter to column index
            if place_checker(board, column, current_player):
                valid_move = True
            else:
                print("Column is full. Please choose another column.")

        print_board(board)

        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            break
        if check_draw(board):
            print("The game is a draw!")
            break

        current_player_index = (current_player_index + 1) % len(PLAYERS)  # Switch turn

# Start the game
if __name__ == "__main__":
    play_game()
