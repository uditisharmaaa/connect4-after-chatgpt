import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 2
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]

# Initialize board
def create_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

# Print board
def print_board(board):
    os.system("clear")
    print("  " + "   ".join(chr(65 + i) for i in range(COLUMNS)))
    print("+---" * COLUMNS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

# Drop checker
def drop_checker(board, column, checker):
    for row in range(ROWS - 1, -1, -1):
        if board[row][column] == " ":
            board[row][column] = checker
            return True
    return False

# Check for win
def check_win(board, checker):
    # Horizontal
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True
    # Vertical
    for row in range(ROWS - 3):
        for col in range(COLUMNS):
            if all(board[row + i][col] == checker for i in range(4)):
                return True
    # Diagonal /
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True
    # Diagonal \
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True
    return False

# Check for draw
def check_draw(board):
    return all(board[0][col] != " " for col in range(COLUMNS))

# Main game loop
def play_game():
    board = create_board()
    players = [PLAYER_CHECKERS[i] for i in range(MAX_PLAYERS)]
    current_player = random.randint(0, MAX_PLAYERS - 1)
    
    while True:
        print_board(board)
        print(f"Player {players[current_player]}, please enter a column:")
        choice = input().strip().upper()
        
        if len(choice) == 1 and "A" <= choice <= chr(65 + COLUMNS - 1):
            column = ord(choice) - 65
            if drop_checker(board, column, players[current_player]):
                if check_win(board, players[current_player]):
                    print_board(board)
                    print(f"Player {players[current_player]} won!")
                    break
                if check_draw(board):
                    print_board(board)
                    print("It's a draw!")
                    break
                current_player = (current_player + 1) % MAX_PLAYERS
            else:
                print("Column is full. Try again.")
        else:
            print("Invalid input. Try again.")

# Start game
play_game()
