import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]

# Initialize the board
def create_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

# Print the board
def print_board(board):
    os.system('clear')  # Clear the terminal for better visualization
    print("  " + "   ".join(chr(65 + i) for i in range(COLUMNS)))
    print("+---" * COLUMNS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

# Check if the input column is valid
def is_valid_column(column, board):
    if len(column) != 1 or not column.isalpha():
        return False
    col_index = ord(column.upper()) - 65
    return 0 <= col_index < COLUMNS and board[0][col_index] == " "

# Place a checker in the column
def place_checker(column, player, board):
    col_index = ord(column.upper()) - 65
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = player
            return True
    return False

# Check for a win condition
def check_for_win(board, player):
    # Horizontal check
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col + i] == player for i in range(4)):
                return True
    # Vertical check
    for row in range(ROWS - 3):
        for col in range(COLUMNS):
            if all(board[row + i][col] == player for i in range(4)):
                return True
    # Diagonal (top-left to bottom-right)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == player for i in range(4)):
                return True
    # Diagonal (bottom-left to top-right)
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row - i][col + i] == player for i in range(4)):
                return True
    return False

# Check for a draw condition
def check_for_draw(board):
    return all(board[0][col] != " " for col in range(COLUMNS))

# Main game loop
def play_game():
    # Initialize the board and players
    board = create_board()
    num_players = 2  # Set the number of players
    players = PLAYER_CHECKERS[:num_players]
    current_player = random.choice(players)
    
    print_board(board)
    print(f"Randomly selected player {current_player} starts!")

    while True:
        # Ask the current player for input
        while True:
            column = input(f"Player {current_player}, please enter a column: ").strip().upper()
            if is_valid_column(column, board):
                break
            print("Invalid input. Please enter a valid column.")
        
        # Place the checker
        place_checker(column, current_player, board)

        # Print the updated board
        print_board(board)

        # Check for a win
        if check_for_win(board, current_player):
            print(f"Player {current_player} won!")
            break

        # Check for a draw
        if check_for_draw(board):
            print("The game is a draw!")
            break

        # Switch to the next player
        current_player = players[(players.index(current_player) + 1) % num_players]

if __name__ == "__main__":
    play_game()
