import os
import random

# Constants
ROWS = 6
COLS = 7
MAX_PLAYERS = 5
PLAYERS = ["X", "O", "V", "H", "M"]

def initialize_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')  # Clear the terminal screen
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))  # Column labels A-G
    print("+---" + "---+" * COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" + "---+" * COLS)

def get_valid_input(player):
    while True:
        col = input(f"Player {player}, please enter a column (A-G): ").strip().upper()
        if len(col) == 1 and 'A' <= col <= 'G':
            col_index = ord(col) - 65  # Convert A-G to 0-6
            return col_index
        else:
            print("Invalid input. Please enter a valid column letter (A-G).")

def place_checker(board, col, checker):
    for row in reversed(board):  # Start from the bottom of the column
        if row[col] == " ":
            row[col] = checker
            return True
    return False  # Column is full

def check_winner(board, checker):
    # Check horizontal
    for row in board:
        for col in range(COLS - 3):
            if all(row[col + i] == checker for i in range(4)):
                return True
    
    # Check vertical
    for col in range(COLS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == checker for i in range(4)):
                return True

    # Check diagonal (bottom-left to top-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True

    # Check diagonal (top-left to bottom-right)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True

    return False

def is_draw(board):
    return all(cell != " " for row in board for cell in row)

def main():
    board = initialize_board()
    players = PLAYERS[:2]  # For this assignment, always use 2 players
    current_player_index = random.randint(0, 1)  # Randomly select the first player

    print_board(board)

    while True:
        current_player = players[current_player_index]
        col = get_valid_input(current_player)
        
        if place_checker(board, col, current_player):
            print_board(board)
            if check_winner(board, current_player):
                print(f"Player {current_player} won!")
                break
            if is_draw(board):
                print("The game is a draw!")
                break
        
            current_player_index = (current_player_index + 1) % len(players)  # Switch player
        else:
            print("Column is full. Please choose another column.")

if __name__ == "__main__":
    main()
