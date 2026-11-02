import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O', 'V', 'H', 'M']

# Create the board
def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

# Print the board
def print_board(board):
    os.system('clear')
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))
    print("+" + "---+" * COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)
    
# Get player input
def get_valid_input(current_player):
    while True:
        try:
            col_input = input(f"Player {current_player}, please enter a column (A-G): ").upper()
            if len(col_input) == 1 and col_input >= 'A' and col_input < chr(65 + COLS):
                return ord(col_input) - 65
            else:
                print("Invalid input. Please try again.")
        except ValueError:
            print("Invalid input. Please try again.")

# Place a checker in the board
def place_checker(board, column, checker):
    for row in reversed(board):
        if row[column] == " ":
            row[column] = checker
            return True
    return False

# Check for a win
def check_win(board, checker):
    # Check horizontal, vertical and diagonal directions
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == checker:
                # Check horizontal
                if col + 3 < COLS and all(board[row][col + i] == checker for i in range(4)):
                    return True
                # Check vertical
                if row + 3 < ROWS and all(board[row + i][col] == checker for i in range(4)):
                    return True
                # Check diagonal (bottom-left to top-right)
                if row >= 3 and col + 3 < COLS and all(board[row - i][col + i] == checker for i in range(4)):
                    return True
                # Check diagonal (top-left to bottom-right)
                if row + 3 < ROWS and col + 3 < COLS and all(board[row + i][col + i] == checker for i in range(4)):
                    return True
    return False

# Check for a draw
def check_draw(board):
    return all(board[0][col] != " " for col in range(COLS))

# Main game logic
def play_game():
    board = create_board()
    current_player_index = random.randint(0, len(PLAYERS) - 1)
    total_players = len(PLAYERS)

    while True:
        print_board(board)
        current_player = PLAYERS[current_player_index]
        column = get_valid_input(current_player)

        if place_checker(board, column, current_player):
            if check_win(board, current_player):
                print_board(board)
                print(f"Player {current_player} won!")
                break
            if check_draw(board):
                print_board(board)
                print("The game is a draw!")
                break
            current_player_index = (current_player_index + 1) % total_players
        else:
            print("Column is full, please try again.")

if __name__ == "__main__":
    play_game()
