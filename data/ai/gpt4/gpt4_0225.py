import os
import random

# Constants
ROWS = 6
COLS = 7
MAX_PLAYERS = 5
PLAYERS = ["X", "O", "V", "H", "M"]  # Checker symbols for players

# Create and initialize the game board
def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

# Print the game board
def print_board(board):
    os.system('clear')
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))
    print("+---" * COLS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLS + "+")

# Check if a move is valid
def is_valid_move(column, board):
    return 0 <= column < COLS and board[0][column] == " "

# Place a checker in the chosen column
def place_checker(board, column, checker):
    for row in range(ROWS - 1, -1, -1):
        if board[row][column] == " ":
            board[row][column] = checker
            return

# Check for a win condition (horizontal, vertical, diagonal)
def check_win(board, checker):
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True

    # Check vertical
    for col in range(COLS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == checker for i in range(4)):
                return True

    # Check diagonal (down-right \)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True

    # Check diagonal (up-right /)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True

    return False

# Check if the board is full (draw)
def is_draw(board):
    return all(board[0][col] != " " for col in range(COLS))

# Main Connect 4 function
def connect_4():
    # Initialize the game board
    board = create_board()

    # Number of players
    num_players = 2  # Change this for more players, up to MAX_PLAYERS
    checkers = PLAYERS[:num_players]

    # Randomly select the first player
    current_player_idx = random.randint(0, num_players - 1)

    # Game loop
    while True:
        print_board(board)
        current_player = checkers[current_player_idx]
        print(f"Player {current_player}, please enter a column:")

        # Get valid player input
        while True:
            try:
                user_input = input("> ").strip().upper()
                if len(user_input) != 1 or not ("A" <= user_input <= chr(65 + COLS - 1)):
                    raise ValueError("Invalid input. Please enter a valid column letter.")
                column = ord(user_input) - 65
                if not is_valid_move(column, board):
                    raise ValueError("Column is full or invalid. Choose a different column.")
                break
            except ValueError as e:
                print(e)

        # Place the checker
        place_checker(board, column, current_player)

        # Check for a win or draw
        if check_win(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break
        elif is_draw(board):
            print_board(board)
            print("It's a draw!")
            break

        # Switch to the next player
        current_player_idx = (current_player_idx + 1) % num_players

if __name__ == "__main__":
    connect_4()
