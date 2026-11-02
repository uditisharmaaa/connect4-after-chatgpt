import random
import os

# Constants
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
PLAYERS = ["X", "O", "V", "H", "M"]

# Create the board
def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

# Print the board
def print_board(board):
    os.system('clear')
    
    # Print column letters
    print("  " + "   ".join(chr(ord('A') + i) for i in range(COLUMNS)))
    print("+" + "---+" * COLUMNS)
    
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLUMNS)

# Place checker in column
def place_checker(board, column, player):
    for row in reversed(board):
        if row[column] == " ":
            row[column] = player
            return True
    return False

# Check if input is valid
def is_valid_input(input_str, max_col):
    if len(input_str) == 1 and input_str.isalpha():
        column = ord(input_str.upper()) - ord('A')
        return 0 <= column < max_col
    return False

# Check for win condition
def check_win(board, player):
    # Check horizontal
    for row in board:
        for col in range(COLUMNS - 3):
            if all(cell == player for cell in row[col:col+4]):
                return True
    
    # Check vertical
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row+i][col] == player for i in range(4)):
                return True
    
    # Check diagonal (bottom left to top right)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row+i][col+i] == player for i in range(4)):
                return True
    
    # Check diagonal (top left to bottom right)
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row-i][col+i] == player for i in range(4)):
                return True
    
    return False

# Check for draw condition
def check_draw(board):
    return all(cell != " " for row in board for cell in row)

# Main Game Function
def connect4_game():
    board = create_board(ROWS, COLUMNS)
    num_players = 2  # Can be set to any number between 2 and MAX_PLAYERS
    current_turn = random.randint(0, num_players - 1)
    
    print_board(board)
    
    while True:
        player = PLAYERS[current_turn]
        print(f"Player {player}, please enter a column:")
        
        while True:
            user_input = input().strip()
            if is_valid_input(user_input, COLUMNS):
                column = ord(user_input.upper()) - ord('A')
                if place_checker(board, column, player):
                    break
                else:
                    print("Column is full! Player loses turn.")
                    break
            else:
                print("Invalid input! Please enter a valid column letter.")
        
        print_board(board)
        
        if check_win(board, player):
            print(f"Player {player} won!")
            break
        
        if check_draw(board):
            print("The game is a draw!")
            break
        
        current_turn = (current_turn + 1) % num_players

# Start the Connect 4 game
connect4_game()
