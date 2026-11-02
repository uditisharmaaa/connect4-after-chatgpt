import os
import random

# Constants for the game
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O']

# Create the board
def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

# Print the board
def print_board(board):
    os.system('clear')  # Clear the screen
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))  # Column labels A, B, C, D, ...
    print("+" + "---+" * COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)

# Check for a valid move
def is_valid_move(board, col):
    return board[0][col] == ' '

# Place the checker in the board at the specified column
def place_checker(board, col, checker):
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = checker
            return True
    return False

# Check for a win condition
def check_win(board, checker):
    # Check horizontal
    for r in range(ROWS):
        for c in range(COLS - 3):
            if all(board[r][c + i] == checker for i in range(4)):
                return True

    # Check vertical
    for r in range(ROWS - 3):
        for c in range(COLS):
            if all(board[r + i][c] == checker for i in range(4)):
                return True

    # Check diagonal (bottom-left to top-right)
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if all(board[r + i][c + i] == checker for i in range(4)):
                return True
            
    # Check diagonal (top-left to bottom-right)
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if all(board[r - i][c + i] == checker for i in range(4)):
                return True

    return False

# Check for a draw
def is_draw(board):
    return all(board[0][c] != ' ' for c in range(COLS))

# Main game function
def play_game():
    board = create_board()
    current_player = random.choice(PLAYERS)
    game_over = False
    
    while not game_over:
        print_board(board)
        print(f"Player {current_player}, please enter a column (A-G): ")
        
        while True:
            user_input = input().strip()
            if len(user_input) == 1 and user_input.isalpha():
                col = ord(user_input.upper()) - 65
                if 0 <= col < COLS and is_valid_move(board, col):
                    break
                else:
                    print("Invalid input. Try again.")
            else:
                print("Invalid input. Try again.")
        
        place_checker(board, col, current_player)
        
        if check_win(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            game_over = True
        elif is_draw(board):
            print_board(board)
            print("The game is a draw!")
            game_over = True
        else:
            current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % len(PLAYERS)]

if __name__ == "__main__":
    play_game()
