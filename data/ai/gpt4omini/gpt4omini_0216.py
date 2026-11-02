import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')  # Clear the terminal
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))  # Column labels A, B, C, ...
    print("+" + "---+" * COLS)  # Top border
    for row in board:
        print("| " + " | ".join(row) + " |")  # Row contents
        print("+" + "---+" * COLS)  # Bottom border

def is_valid_input(col_input):
    return len(col_input) == 1 and 'A' <= col_input <= chr(65 + COLS - 1)

def find_lowest_empty_row(board, col):
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            return row
    return -1

def check_win(board, player):
    # Check horizontal, vertical, and diagonal wins
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == player:
                if c + 3 < COLS and all(board[r][c + i] == player for i in range(4)):  # Horizontal
                    return True
                if r + 3 < ROWS and all(board[r + i][c] == player for i in range(4)):  # Vertical
                    return True
                if c + 3 < COLS and r + 3 < ROWS and all(board[r + i][c + i] == player for i in range(4)):  # Diagonal \
                    return True
                if c - 3 >= 0 and r + 3 < ROWS and all(board[r + i][c - i] == player for i in range(4)):  # Diagonal /
                    return True
    return False

def is_draw(board):
    return all(board[0][c] != " " for c in range(COLS))

def play_game():
    board = create_board()
    current_player = random.choice(PLAYERS[:2])  # Randomly select the first player
    print_board(board)
    
    while True:
        # Get valid column input from the current player
        while True:
            col_input = input(f"Player {current_player}, please enter a column (A-{chr(64 + COLS)}): ").upper()
            if is_valid_input(col_input):
                col = ord(col_input) - 65
                row = find_lowest_empty_row(board, col)
                if row != -1:
                    board[row][col] = current_player
                    break
                else:
                    print("Column is full, please try another column.")
            else:
                print("Invalid input, please enter a letter corresponding to a column.")

        print_board(board)

        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            break
        elif is_draw(board):
            print("The game is a draw!")
            break
        
        # Switch player
        current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % len(PLAYERS)]

if __name__ == "__main__":
    play_game()
