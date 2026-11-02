import os
import random

# Constants for the game
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
PLAYERS = ['X', 'O', 'V', 'H', 'M']  # Player symbols

# Function to create a new game board
def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

# Function to clear the console screen
def clear_screen():
    os.system('clear')

# Function to print the game board
def print_board(board):
    clear_screen()
    print("  " + "   ".join(chr(65 + i) for i in range(len(board[0]))))  # Print column headers
    print("+---" * len(board[0]) + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * len(board[0]) + "+")

# Function to check if the column is valid for a play
def is_valid_column(board, col):
    if len(col) != 1 or not col.isalpha():
        return False
    col_index = ord(col.upper()) - 65
    return 0 <= col_index < len(board[0]) and board[0][col_index] == " "

# Function to drop a checker into a column
def drop_checker(board, col, player):
    col_index = ord(col.upper()) - 65
    for row in reversed(board):
        if row[col_index] == " ":
            row[col_index] = player
            break

# Function to check for a win
def check_win(board, player):
    rows, cols = len(board), len(board[0])
    # Check horizontal
    for row in range(rows):
        for col in range(cols - 3):
            if all(board[row][col + i] == player for i in range(4)):
                return True
    # Check vertical
    for col in range(cols):
        for row in range(rows - 3):
            if all(board[row + i][col] == player for i in range(4)):
                return True
    # Check diagonal (down-right)
    for row in range(rows - 3):
        for col in range(cols - 3):
            if all(board[row + i][col + i] == player for i in range(4)):
                return True
    # Check diagonal (up-right)
    for row in range(3, rows):
        for col in range(cols - 3):
            if all(board[row - i][col + i] == player for i in range(4)):
                return True
    return False

# Function to check for a draw (when the board is full)
def check_draw(board):
    return all(cell != " " for row in board for cell in row)

# Function to rotate players in turn
def next_player(players, current_player_index):
    return (current_player_index + 1) % len(players)

# Main function to play the game
def play_game():
    # Initialize the board
    board = create_board(ROWS, COLUMNS)

    # Number of players (hardcoded to 2 as per assignment)
    num_players = 2  # For submission, initially set to 2 players
    # Select players
    players = PLAYERS[:num_players]

    # Randomly select the first player
    current_player_index = random.randint(0, num_players - 1)

    # Start the game loop
    while True:
        # Print the board
        print_board(board)

        # Get the current player
        current_player = players[current_player_index]
        print(f"Player {current_player}, it's your turn!")

        # Ask for a valid column
        while True:
            column_input = input("Please enter a column (A-G): ").strip().upper()
            if is_valid_column(board, column_input):
                break
            else:
                print("Invalid column. Please try again.")

        # Drop the checker into the column
        drop_checker(board, column_input, current_player)

        # Check for a win or a draw
        if check_win(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break
        elif check_draw(board):
            print_board(board)
            print("The game is a draw!")
            break

        # Move to the next player
        current_player_index = next_player(players, current_player_index)

# Run the game
if __name__ == "__main__":
    play_game()
