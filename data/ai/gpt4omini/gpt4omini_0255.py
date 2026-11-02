import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O', 'V', 'H', 'M']  # Up to 5 players

# Create the game board
def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

# Print the game board
def print_board(board):
    os.system('clear')  # Clear the console
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))
    print("+" + "---+" * COLS)
    
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)

# Check if the column is valid
def is_valid_column(board, col):
    return 0 <= col < COLS and board[0][col] == ' '

# Place the checker in the specified column
def place_checker(board, col, player):
    for row in reversed(board):  # Start from the bottom of the column
        if row[col] == ' ':
            row[col] = player
            return True
    return False  # Column is full

# Check for a win
def check_win(board, player):
    return (check_horizontal(board, player) or
            check_vertical(board, player) or
            check_diagonal(board, player))

def check_horizontal(board, player):
    for row in board:
        count = 0
        for cell in row:
            count = count + 1 if cell == player else 0
            if count >= 4:
                return True
    return False

def check_vertical(board, player):
    for col in range(COLS):
        count = 0
        for row in range(ROWS):
            count = count + 1 if board[row][col] == player else 0
            if count >= 4:
                return True
    return False

def check_diagonal(board, player):
    # Check for diagonals from bottom-left to top-right
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == player:
                if (col + 3 < COLS and row - 3 >= 0 and
                        board[row - 1][col + 1] == player and
                        board[row - 2][col + 2] == player and
                        board[row - 3][col + 3] == player):
                    return True

    # Check for diagonals from bottom-right to top-left
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == player:
                if (col - 3 >= 0 and row - 3 >= 0 and
                        board[row - 1][col - 1] == player and
                        board[row - 2][col - 2] == player and
                        board[row - 3][col - 3] == player):
                    return True

    return False

# Check for a draw
def check_draw(board):
    return all(board[0][col] != ' ' for col in range(COLS))

# Main game loop
def play_game():
    board = create_board()
    current_player_index = random.randint(0, len(PLAYERS) - 1)

    while True:
        print_board(board)
        current_player = PLAYERS[current_player_index]
        print(f"Player {current_player}, please enter a column (A-G): ")

        valid_input = False
        while not valid_input:
            user_input = input().upper()
            if len(user_input) == 1 and user_input.isalpha():
                column = ord(user_input) - 65
                if is_valid_column(board, column):
                    place_checker(board, column, current_player)
                    valid_input = True
                else:
                    print("Column is full, please choose another column.")
            else:
                print("Invalid input, please enter a letter from A to G.")

        if check_win(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break

        if check_draw(board):
            print_board(board)
            print("The game is a draw!")
            break

        current_player_index = (current_player_index + 1) % len(PLAYERS)

if __name__ == "__main__":
    play_game()
