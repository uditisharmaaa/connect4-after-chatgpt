import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = ["X", "O"]  # You can change this to include more players if needed

# Function to create the board
def create_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

# Function to print the board
def print_board(board):
    os.system('clear')  # Clear the terminal screen
    print("  " + "   ".join(chr(65 + i) for i in range(COLUMNS)))  # Column headers
    print("+---" * COLUMNS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

# Function to check if a column is valid for the move
def is_valid_move(board, col):
    return col >= 0 and col < COLUMNS and board[0][col] == " "

# Function to get the next available row in a column
def get_next_row(board, col):
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == " ":
            return r
    return -1

# Function to check for a win
def check_win(board, player):
    # Check horizontal
    for r in range(ROWS):
        for c in range(COLUMNS - 3):
            if all(board[r][c + i] == player for i in range(4)):
                return True

    # Check vertical
    for c in range(COLUMNS):
        for r in range(ROWS - 3):
            if all(board[r + i][c] == player for i in range(4)):
                return True

    # Check diagonal (increasing)
    for r in range(ROWS - 3):
        for c in range(COLUMNS - 3):
            if all(board[r + i][c + i] == player for i in range(4)):
                return True

    # Check diagonal (decreasing)
    for r in range(3, ROWS):
        for c in range(COLUMNS - 3):
            if all(board[r - i][c + i] == player for i in range(4)):
                return True

    return False

# Function to check for a draw
def check_draw(board):
    return all(board[0][c] != " " for c in range(COLUMNS))

# Main game loop
def play_game():
    board = create_board()
    current_player_index = random.randint(0, len(PLAYERS) - 1)

    while True:
        print_board(board)
        current_player = PLAYERS[current_player_index]
        print(f"Player {current_player}, please enter a column (A-G): ")

        col_input = input().upper()
        if len(col_input) != 1 or col_input < 'A' or col_input > chr(65 + COLUMNS - 1):
            print("Invalid column. Please try again.")
            continue
        
        col = ord(col_input) - 65
        
        if not is_valid_move(board, col):
            print("That column is full. Please try again.")
            continue

        # Place the checker
        row = get_next_row(board, col)
        board[row][col] = current_player

        # Check for win
        if check_win(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break

        # Check for draw
        if check_draw(board):
            print_board(board)
            print("The game is a draw!")
            break

        # Switch player
        current_player_index = (current_player_index + 1) % len(PLAYERS)

# Start the game
if __name__ == "__main__":
    play_game()
