import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
MIN_PLAYERS = 2
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]

# Initialize board
def create_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]

# Print the board
def display_board(board):
    os.system('clear')  # Clear the terminal
    col_labels = "   ".join(chr(65 + i) for i in range(len(board[0])))
    print("  " + col_labels)
    print("+---" * len(board[0]) + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * len(board[0]) + "+")

# Check for a win
def check_for_win(board, symbol):
    # Check horizontal, vertical, and diagonal wins
    rows, cols = len(board), len(board[0])
    for row in range(rows):
        for col in range(cols):
            if col + 3 < cols and all(board[row][c] == symbol for c in range(col, col + 4)):
                return True
            if row + 3 < rows and all(board[r][col] == symbol for r in range(row, row + 4)):
                return True
            if col + 3 < cols and row + 3 < rows and all(board[row+i][col+i] == symbol for i in range(4)):
                return True
            if col - 3 >= 0 and row + 3 < rows and all(board[row+i][col-i] == symbol for i in range(4)):
                return True
    return False

# Check for a draw (full board)
def check_for_draw(board):
    return all(cell != " " for row in board for cell in row)

# Place checker on the board
def place_checker(board, column, symbol):
    for row in reversed(board):
        if row[column] == " ":
            row[column] = symbol
            return True
    return False

# Get valid user input
def get_valid_input(columns):
    while True:
        user_input = input("Please enter a column: ").upper()
        if len(user_input) == 1 and 'A' <= user_input <= chr(65 + columns - 1):
            return ord(user_input) - 65
        print("Invalid input. Try again.")

# Main connect 4 function
def connect_4():
    # Setup game
    num_players = 2
    players = PLAYER_SYMBOLS[:num_players]
    board = create_board(ROWS, COLUMNS)
    current_player_index = random.randint(0, num_players - 1)
    is_game_over = False

    display_board(board)
    print(f"Player {players[current_player_index]} goes first!")

    # Game loop
    while not is_game_over:
        current_player = players[current_player_index]
        print(f"Player {current_player}'s turn.")
        column = get_valid_input(COLUMNS)

        # Attempt to place checker
        if place_checker(board, column, current_player):
            display_board(board)
            # Check for a win
            if check_for_win(board, current_player):
                print(f"Player {current_player} won!")
                is_game_over = True
            # Check for a draw
            elif check_for_draw(board):
                print("It's a draw!")
                is_game_over = True
            else:
                # Switch to next player
                current_player_index = (current_player_index + 1) % num_players
        else:
            print("Column is full. Try another column.")

if __name__ == "__main__":
    connect_4()
