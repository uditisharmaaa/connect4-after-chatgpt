import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = ["X", "O", "V", "H", "M"]
PLAYER_COUNT = 2  # Change this to 2, 3, 4, or 5

# Functions to display the board
def display_board(board):
    os.system('clear')  # Use 'cls' on Windows
    print(" A B C D E F G")
    for row in board:
        print("|".join(row))
    print("---------------")

# Initialize the board
def create_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

# Validate input
def validate_input(choice, board):
    col_index = ord(choice.upper()) - ord('A')
    return 0 <= col_index < COLUMNS and board[0][col_index] == " "

# Check for a win
def check_win(board, symbol):
    # Check horizontal, vertical, and diagonal wins
    for row in range(ROWS):
        for col in range(COLUMNS - 3):  # horizontal
            if all(board[row][col + i] == symbol for i in range(4)):
                return True
    for row in range(ROWS - 3):
        for col in range(COLUMNS):  # vertical
            if all(board[row + i][col] == symbol for i in range(4)):
                return True
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):  # diagonal /
            if all(board[row + i][col + i] == symbol for i in range(4)):
                return True
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):  # diagonal \
            if all(board[row - i][col + i] == symbol for i in range(4)):
                return True
    return False

# Check for a draw
def check_draw(board):
    return all(board[0][col] != " " for col in range(COLUMNS))

# Place a piece on the board
def place_piece(board, choice, symbol):
    col_index = ord(choice.upper()) - ord('A')
    for row in reversed(range(ROWS)):
        if board[row][col_index] == " ":
            board[row][col_index] = symbol
            break

# Main game loop
def connect4():
    board = create_board()
    players = PLAYERS[:PLAYER_COUNT]
    current_player_index = random.randint(0, PLAYER_COUNT - 1)
    
    while True:
        display_board(board)
        current_player = players[current_player_index]
        print(f"Player {current_player}'s turn.")
        
        # Validate input
        move = input("Choose a column (A-G): ")
        while not validate_input(move, board):
            move = input("Invalid move. Choose a column (A-G): ")
        
        # Place piece and check game state
        place_piece(board, move, current_player)
        
        if check_win(board, current_player):
            display_board(board)
            print(f"Player {current_player} wins!")
            break
        elif check_draw(board):
            display_board(board)
            print("It's a draw!")
            break
        
        # Switch to next player
        current_player_index = (current_player_index + 1) % PLAYER_COUNT

if __name__ == "__main__":
    connect4()
