import os
import random

# Constants for board dimensions and players
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O']  # Add more players if needed

def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')  # Clear the terminal screen
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))
    print("+" + "---+" * COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)

def get_valid_input(player):
    while True:
        inp = input(f"Player {player}, please enter a column (A-{chr(65 + COLS - 1)}): ").upper()
        
        if len(inp) != 1 or not (65 <= ord(inp) < 65 + COLS):
            print("Invalid input! Please enter a valid column letter.")
            continue
        
        col = ord(inp) - 65
        if board[0][col] != " ":
            print("Column is full! Please choose another column.")
        else:
            return col

def place_checker(board, col, player):
    for row in reversed(board):  # Start from the bottom
        if row[col] == " ":
            row[col] = player
            break

def check_winner(board):
    # Check horizontal, vertical, and diagonal wins
    for r in range(ROWS):
        for c in range(COLS):
            # Check horizontal
            if c + 3 < COLS and all(board[r][c + i] == board[r][c] != " " for i in range(4)):
                return True
            # Check vertical
            if r + 3 < ROWS and all(board[r + i][c] == board[r][c] != " " for i in range(4)):
                return True
            # Check diagonal (bottom left to top right)
            if r - 3 >= 0 and c + 3 < COLS and all(board[r - i][c + i] == board[r][c] != " " for i in range(4)):
                return True
            # Check diagonal (top left to bottom right)
            if r + 3 < ROWS and c + 3 < COLS and all(board[r + i][c + i] == board[r][c] != " " for i in range(4)):
                return True
    return False

def check_draw(board):
    return all(board[0][c] != " " for c in range(COLS))

# Main game loop
board = create_board()
current_player = random.choice(PLAYERS)
print_board(board)

while True:
    col = get_valid_input(current_player)
    place_checker(board, col, current_player)
    print_board(board)

    if check_winner(board):
        print(f"Player {current_player} won!")
        break
    if check_draw(board):
        print("The game is a draw!")
        break
    
    # Switch players
    current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % len(PLAYERS)]
