import os
import random

# Global constants
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
PLAYER_TOKENS = ['X', 'O', 'V', 'H', 'M']

# Function to create and initialize the board
def create_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]

# Function to print the board
def print_board(board):
    os.system('clear')  # Clears the terminal screen
    column_labels = "  " + "   ".join([chr(ord('A') + i) for i in range(COLUMNS)])
    print(column_labels)
    print("+---" * COLUMNS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

# Function to check if a move is valid
def is_valid_move(column_input, board):
    if column_input < 0 or column_input >= COLUMNS:
        return False
    return board[0][column_input] == " "

# Function to place a player's checker on the board
def place_checker(board, column, player_token):
    for row in reversed(board):
        if row[column] == " ":
            row[column] = player_token
            break

# Function to check for a win condition
def check_winner(board, player_token):
    # Horizontal check
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col + i] == player_token for i in range(4)):
                return True

    # Vertical check
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == player_token for i in range(4)):
                return True

    # Diagonal check (descending)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == player_token for i in range(4)):
                return True

    # Diagonal check (ascending)
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row - i][col + i] == player_token for i in range(4)):
                return True

    return False

# Function to check for a draw
def check_draw(board):
    return all(board[0][col] != " " for col in range(COLUMNS))

# Function to get a validated input column from a player
def get_player_move(player, board):
    while True:
        try:
            column_input = input(f"Player {player}, please enter a column: ").strip().upper()
            if len(column_input) != 1 or not column_input.isalpha():
                raise ValueError("Please enter a single valid column letter.")
            column = ord(column_input) - ord('A')
            if not is_valid_move(column, board):
                raise ValueError("Invalid move. Column is either full or out of range.")
            return column
        except ValueError as e:
            print(e)

# Main game loop
def play_game():
    # Initialize the board
    board = create_board(ROWS, COLUMNS)
    
    # Set the number of players and assign tokens
    num_players = 2  # Default to 2 players as per instructions
    players = PLAYER_TOKENS[:num_players]
    
    # Randomly select the first player
    current_player_index = random.randint(0, num_players - 1)
    
    print_board(board)
    
    while True:
        # Get the current player's token
        current_player = players[current_player_index]

        # Get the player's move
        column = get_player_move(current_player, board)

        # Place the checker on the board
        place_checker(board, column, current_player)

        # Print the updated board
        print_board(board)

        # Check for a win
        if check_winner(board, current_player):
            print(f"Player {current_player} won!")
            break

        # Check for a draw
        if check_draw(board):
            print("The game is a draw!")
            break

        # Switch to the next player
        current_player_index = (current_player_index + 1) % num_players

# Run the game
if __name__ == "__main__":
    play_game()
