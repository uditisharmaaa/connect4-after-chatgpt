import os
import random

# Constants for the game
ROWS = 6
COLS = 7
PLAYER_COUNT = 2
PLAYERS = ['X', 'O']  # Extend to ['X', 'O', 'V', 'H', 'M'] for more players

# Create the board
def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

# Print the board
def print_board(board):
    os.system('clear')
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))  # Column letters A-G
    print("+---" + "---+" * COLS)  # Top border
    for row in board:
        print("| " + " | ".join(row) + " |")  # Row content
        print("+---" + "---+" * COLS)  # Row border

# Check for a win
def check_win(board, player):
    # Check horizontal, vertical, and diagonal wins
    for r in range(ROWS):
        for c in range(COLS):
            if c + 3 < COLS and all(board[r][c + i] == player for i in range(4)):  # Horizontal
                return True
            if r + 3 < ROWS and all(board[r + i][c] == player for i in range(4)):  # Vertical
                return True
            if r + 3 < ROWS and c + 3 < COLS and all(board[r + i][c + i] == player for i in range(4)):  # Diagonal \
                return True
            if r - 3 >= 0 and c + 3 < COLS and all(board[r - i][c + i] == player for i in range(4)):  # Diagonal /
                return True
    return False

# Check for a draw
def check_draw(board):
    return all(board[0][c] != ' ' for c in range(COLS))

# Get user input
def get_input(current_player):
    while True:
        column = input(f"Player {current_player}, please enter a column: ").upper()
        if column in (chr(65 + i) for i in range(COLS)):
            return ord(column) - 65
        print("Invalid input. Please enter a valid column letter (A-G).")

# Place the checker on the board
def place_checker(board, column, player):
    for row in reversed(board):  # Start from the bottom row
        if row[column] == ' ':
            row[column] = player
            return True
    return False

# Main game loop
def play_game():
    board = create_board()
    current_player_index = random.randint(0, PLAYER_COUNT - 1)
    
    while True:
        print_board(board)
        current_player = PLAYERS[current_player_index]
        
        column = get_input(current_player)
        if not place_checker(board, column, current_player):
            print("Column is full! Please choose another column.")
            continue  # Skip to the next turn if the column is full

        if check_win(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break
        if check_draw(board):
            print_board(board)
            print("The game is a draw!")
            break
        
        current_player_index = (current_player_index + 1) % PLAYER_COUNT  # Switch to the next player

if __name__ == "__main__":
    play_game()
