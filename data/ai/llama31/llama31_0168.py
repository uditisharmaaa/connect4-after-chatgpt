import os
import random

# Constants
BOARD_WIDTH = 7
BOARD_HEIGHT = 6
CHECKERS = ["X", "O", "V", "H", "M"]
NUM_PLAYERS = 2

def create_board(width, height):
    """Create a new game board with the specified width and height."""
    return [[" " for _ in range(width)] for _ in range(height)]

def print_board(board, current_player):
    """Print the current state of the board."""
    os.system('clear')
    print("  A B C D E F G")
    for row in range(len(board)):
        print("+---" * len(board[row]) + "+")
        print("|", end="")
        for col in range(len(board[row])):
            print(" " + board[row][col] + " |", end="")
        print()
    print("+---" * len(board[row]) + "+")
    print(f"Player {CHECKERS[current_player]}, please enter a column (A-G): ")

def get_player_input(current_player):
    """Get the player's input and validate it."""
    while True:
        user_input = input().upper()
        if len(user_input)!= 1 or not 'A' <= user_input <= 'G':
            print("Invalid input. Please enter a letter between A and G.")
            continue
        col = ord(user_input) - ord('A')
        if board[0][col]!= " ":
            print("Column is full. Please choose another column.")
            continue
        return col

def place_checker(board, player, col):
    """Place the player's checker in the specified column."""
    for row in range(len(board) - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = CHECKERS[player]
            return

def check_win(board, player):
    """Check if the player has won."""
    # Check horizontal
    for row in range(len(board)):
        for col in range(len(board[row]) - 3):
            if board[row][col] == board[row][col + 1] == board[row][col + 2] == board[row][col + 3] == CHECKERS[player]:
                return True

    # Check vertical
    for row in range(len(board) - 3):
        for col in range(len(board[row])):
            if board[row][col] == board[row + 1][col] == board[row + 2][col] == board[row + 3][col] == CHECKERS[player]:
                return True

    # Check diagonal (top-left to bottom-right)
    for row in range(len(board) - 3):
        for col in range(len(board[row]) - 3):
            if board[row][col] == board[row + 1][col + 1] == board[row + 2][col + 2] == board[row + 3][col + 3] == CHECKERS[player]:
                return True

    # Check diagonal (bottom-left to top-right)
    for row in range(3, len(board)):
        for col in range(len(board[row]) - 3):
            if board[row][col] == board[row - 1][col + 1] == board[row - 2][col + 2] == board[row - 3][col + 3] == CHECKERS[player]:
                return True

    return False

def check_draw(board):
    """Check if the game is a draw."""
    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] == " ":
                return False
    return True

# Initialize the game
board = create_board(BOARD_WIDTH, BOARD_HEIGHT)
current_player = random.randint(0, NUM_PLAYERS - 1)

# Main game loop
while True:
    print_board(board, current_player)
    col = get_player_input(current_player)
    place_checker(board, current_player, col)

    if check_win(board, current_player):
        print_board(board, current_player)
        print(f"Player {CHECKERS[current_player]} won!")
        break

    if check_draw(board):
        print_board(board, current_player)
        print("It's a draw!")
        break

    current_player = (current_player + 1) % NUM_PLAYERS
