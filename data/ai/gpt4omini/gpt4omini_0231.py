import os
import random

# Constants for the board dimensions and players
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O', 'V', 'H', 'M']

# Initialize the game board
def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

# Print the game board
def print_board(board):
    os.system('clear')  # Clear the terminal (Linux/Unix)
    print("   " + "   ".join(chr(65 + i) for i in range(COLS)))
    print("+" + "---+" * COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)

# Check if the input from the user is valid
def is_valid_input(col):
    if len(col) != 1 or not col.isalpha():
        return False
    column = ord(col.upper()) - 65
    return 0 <= column < COLS

# Place the checker in the board
def place_checker(board, column, player):
    for row in reversed(board):
        if row[column] == ' ':
            row[column] = player
            return True
    return False  # Column is full

# Check for a win
def check_winner(board, player):
    # Check horizontal, vertical and diagonal lines for win
    for r in range(ROWS):
        for c in range(COLS):
            if (c <= COLS - 4 and all(board[r][c + i] == player for i in range(4))) or \
               (r <= ROWS - 4 and all(board[r + i][c] == player for i in range(4))) or \
               (r <= ROWS - 4 and c <= COLS - 4 and all(board[r + i][c + i] == player for i in range(4))) or \
               (r >= 3 and c <= COLS - 4 and all(board[r - i][c + i] == player for i in range(4))):
                return True
    return False

# Check if the game is a draw
def is_draw(board):
    return all(cell != ' ' for row in board for cell in row)

# Main game function
def connect4():
    board = create_board()
    current_player_index = random.randint(0, len(PLAYERS) - 1)

    while True:
        print_board(board)
        current_player = PLAYERS[current_player_index]
        print(f"Player {current_player}, please enter a column (A-{chr(65 + COLS - 1)}):")
        
        while True:
            move = input().strip().upper()
            if is_valid_input(move):
                col = ord(move) - 65
                if place_checker(board, col, current_player):
                    break
                else:
                    print("Column is full! Please select another column.")
            else:
                print("Invalid input! Please enter a valid column (A-G).")

        if check_winner(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break
        
        if is_draw(board):
            print_board(board)
            print("The game is a draw!")
            break

        current_player_index = (current_player_index + 1) % len(PLAYERS)

if __name__ == "__main__":
    connect4()
