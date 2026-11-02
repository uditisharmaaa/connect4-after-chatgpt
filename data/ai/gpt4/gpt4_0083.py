import os
import random

# Constants
ROWS = 6
COLS = 7
MAX_PLAYERS = 5
PLAYER_TOKENS = ['X', 'O', 'V', 'H', 'M']

# Clear the terminal screen
def clear_screen():
    os.system('clear')

# Initialize the board
def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

# Print the board
def print_board(board):
    clear_screen()
    print("  " + "   ".join(chr(65 + i) for i in range(len(board[0]))))  # Column labels A, B, C, ...
    print("+---" * len(board[0]) + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * len(board[0]) + "+")

# Validate user input for column selection
def validate_column_input(input_char, board):
    if len(input_char) != 1 or not input_char.isalpha():
        return False
    col = ord(input_char.upper()) - ord('A')
    return 0 <= col < len(board[0]) and board[0][col] == " "

# Place the checker in the chosen column
def place_checker(board, col, token):
    for row in reversed(board):
        if row[col] == " ":
            row[col] = token
            return True
    return False

# Check for win condition
def check_win(board, token):
    rows, cols = len(board), len(board[0])
    
    # Check horizontal
    for r in range(rows):
        for c in range(cols - 3):
            if all(board[r][c + i] == token for i in range(4)):
                return True
    
    # Check vertical
    for r in range(rows - 3):
        for c in range(cols):
            if all(board[r + i][c] == token for i in range(4)):
                return True

    # Check diagonal (bottom-left to top-right)
    for r in range(rows - 3):
        for c in range(cols - 3):
            if all(board[r + i][c + i] == token for i in range(4)):
                return True

    # Check diagonal (top-left to bottom-right)
    for r in range(3, rows):
        for c in range(cols - 3):
            if all(board[r - i][c + i] == token for i in range(4)):
                return True
    
    return False

# Check for draw condition
def check_draw(board):
    return all(board[0][c] != " " for c in range(len(board[0])))

# Game loop
def connect_4():
    # Initialize board and players
    board = create_board(ROWS, COLS)
    num_players = 2  # For submission, default is 2 players
    tokens = PLAYER_TOKENS[:num_players]
    current_player = random.randint(0, num_players - 1)

    clear_screen()
    print_board(board)

    while True:
        # Get the current player's token
        player_token = tokens[current_player]
        print(f"Player {player_token}, it's your turn!")
        
        # Prompt for column input
        while True:
            user_input = input("Please enter a column: ").strip().upper()
            if validate_column_input(user_input, board):
                col = ord(user_input) - ord('A')
                break
            else:
                print("Invalid input. Please try again.")
        
        # Place the checker
        place_checker(board, col, player_token)
        print_board(board)

        # Check for win
        if check_win(board, player_token):
            print(f"Player {player_token} won!")
            break

        # Check for draw
        if check_draw(board):
            print("It's a draw!")
            break

        # Switch to the next player
        current_player = (current_player + 1) % num_players

# Run the game
if __name__ == "__main__":
    connect_4()
