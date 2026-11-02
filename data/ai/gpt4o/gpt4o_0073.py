import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]  # Checkers for players 1 to 5

# Initialize the board
def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

# Print the board
def print_board(board):
    os.system('clear')  # Clear the screen
    print("  " + "   ".join(chr(65 + i) for i in range(len(board[0]))))  # Column labels A-G
    print("+---" * len(board[0]) + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * len(board[0]) + "+")

# Check for a win
def check_win(board, rows, cols):
    # Horizontal, vertical, and diagonal checks
    for row in range(rows):
        for col in range(cols):
            if board[row][col] != " ":
                # Horizontal check
                if col <= cols - 4 and all(board[row][col + i] == board[row][col] for i in range(4)):
                    return True
                # Vertical check
                if row <= rows - 4 and all(board[row + i][col] == board[row][col] for i in range(4)):
                    return True
                # Diagonal (left to right) check
                if row <= rows - 4 and col <= cols - 4 and all(board[row + i][col + i] == board[row][col] for i in range(4)):
                    return True
                # Diagonal (right to left) check
                if row <= rows - 4 and col >= 3 and all(board[row + i][col - i] == board[row][col] for i in range(4)):
                    return True
    return False

# Check for a draw
def check_draw(board):
    return all(cell != " " for row in board for cell in row)

# Place a checker in the chosen column
def place_checker(board, column, checker):
    for row in reversed(board):
        if row[column] == " ":
            row[column] = checker
            return True
    return False

# Game loop
def play_game():
    board = create_board(ROWS, COLUMNS)
    current_player = random.randint(0, PLAYERS - 1)
    
    while True:
        print_board(board)
        print(f"Player {CHECKERS[current_player]}, please enter a column:")

        while True:
            try:
                user_input = input().strip().upper()
                if len(user_input) != 1 or not ('A' <= user_input <= chr(65 + COLUMNS - 1)):
                    raise ValueError("Invalid input")
                column = ord(user_input) - ord('A')
                if place_checker(board, column, CHECKERS[current_player]):
                    break
                else:
                    print("Column is full, try another one.")
            except ValueError:
                print("Invalid input, please enter a valid column (A-G).")

        if check_win(board, ROWS, COLUMNS):
            print_board(board)
            print(f"Player {CHECKERS[current_player]} won!")
            break
        
        if check_draw(board):
            print_board(board)
            print("The game is a draw!")
            break

        current_player = (current_player + 1) % PLAYERS

play_game()
