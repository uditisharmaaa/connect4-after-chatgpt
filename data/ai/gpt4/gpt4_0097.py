import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
PLAYER_MARKERS = ["X", "O", "V", "H", "M"]

# Function to initialize the board
def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

# Function to print the board
def print_board(board):
    os.system('clear')  # Clear the screen
    header = "  " + "   ".join(chr(65 + i) for i in range(len(board[0])))  # Column letters
    print(header)
    print("+" + "---+" * len(board[0]))
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * len(board[0]))

# Function to drop a checker into a column
def drop_checker(board, column, marker):
    for row in reversed(board):
        if row[column] == " ":
            row[column] = marker
            return True
    return False

# Function to check for a win
def check_win(board, marker):
    # Check horizontal, vertical, and diagonal (both directions)
    for row in range(ROWS):
        for col in range(COLUMNS):
            if col + 3 < COLUMNS and all(board[row][col + i] == marker for i in range(4)):
                return True
            if row + 3 < ROWS and all(board[row + i][col] == marker for i in range(4)):
                return True
            if row + 3 < ROWS and col + 3 < COLUMNS and all(board[row + i][col + i] == marker for i in range(4)):
                return True
            if row + 3 < ROWS and col - 3 >= 0 and all(board[row + i][col - i] == marker for i in range(4)):
                return True
    return False

# Function to check for a draw
def check_draw(board):
    return all(cell != " " for row in board for cell in row)

# Function to get a valid column from the player
def get_valid_column(board, player):
    while True:
        column_input = input(f"Player {player}, please enter a column: ").strip().upper()
        if len(column_input) != 1 or not column_input.isalpha():
            print("Invalid input. Please enter a letter corresponding to a column.")
            continue
        column = ord(column_input) - 65
        if column < 0 or column >= COLUMNS:
            print("Invalid column. Please choose a valid column.")
            continue
        if board[0][column] != " ":
            print("Column is full. Please choose another column.")
            continue
        return column

# Main function to run the game
def play_game():
    # Initialize the game
    board = create_board(ROWS, COLUMNS)
    players = PLAYER_MARKERS[:2]  # Change number of players here if necessary
    random.shuffle(players)  # Randomize player order
    current_player_index = 0

    # Print initial board
    print_board(board)

    # Game loop
    while True:
        # Current player and their marker
        current_player = players[current_player_index]
        print(f"It's Player {current_player}'s turn.")

        # Get a valid column and place the marker
        column = get_valid_column(board, current_player)
        drop_checker(board, column, current_player)
        print_board(board)

        # Check for a win or draw
        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            break
        if check_draw(board):
            print("The game is a draw!")
            break

        # Switch to the next player
        current_player_index = (current_player_index + 1) % len(players)

# Start the game
if __name__ == "__main__":
    play_game()
