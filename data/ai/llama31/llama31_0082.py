import os
import random

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
MIN_PLAYERS = 2
MAX_PLAYERS = 5
CHECKERS = ["X", "O", "V", "H", "M"]

# Function to create the game board
def create_board():
    board = []
    for _ in range(BOARD_ROWS):
        row = []
        for _ in range(BOARD_COLS):
            row.append(" ")
        board.append(row)
    return board

# Function to print the game board
def print_board(board):
    print("  A", end=" ")
    for col in range(BOARD_COLS - 1):
        print(chr(ord("A") + col + 1), end=" ")
    print()
    print("+---" + "+---" * (BOARD_COLS - 1))
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            print(f"| {board[row][col]} ", end="")
        print("|")
        if row < BOARD_ROWS - 1:
            print("+---" + "+---" * (BOARD_COLS - 1))
    print()

# Function to check for a win
def check_win(board, player):
    # Check horizontal
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS - 3):
            if board[row][col] == player and board[row][col + 1] == player and board[row][col + 2] == player and board[row][col + 3] == player:
                return True

    # Check vertical
    for row in range(BOARD_ROWS - 3):
        for col in range(BOARD_COLS):
            if board[row][col] == player and board[row + 1][col] == player and board[row + 2][col] == player and board[row + 3][col] == player:
                return True

    # Check diagonal (top-left to bottom-right)
    for row in range(BOARD_ROWS - 3):
        for col in range(BOARD_COLS - 3):
            if board[row][col] == player and board[row + 1][col + 1] == player and board[row + 2][col + 2] == player and board[row + 3][col + 3] == player:
                return True

    # Check diagonal (bottom-left to top-right)
    for row in range(3, BOARD_ROWS):
        for col in range(BOARD_COLS - 3):
            if board[row][col] == player and board[row - 1][col + 1] == player and board[row - 2][col + 2] == player and board[row - 3][col + 3] == player:
                return True

    return False

# Function to check for a draw
def check_draw(board):
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == " ":
                return False
    return True

# Main game loop
def play_game():
    num_players = 2
    players = CHECKERS[:num_players]
    board = create_board()
    current_player_index = random.randint(0, num_players - 1)
    current_player = players[current_player_index]

    while True:
        os.system('clear')
        print_board(board)
        print(f"Player {current_player}, please enter a column (A-{chr(ord('A') + BOARD_COLS - 1)}):")
        col_input = input().strip().upper()

        # Validate input
        if len(col_input)!= 1 or not col_input.isalpha():
            print("Invalid input. Please enter a single letter.")
            continue
        col = ord(col_input) - ord('A')
        if col < 0 or col >= BOARD_COLS:
            print("Invalid input. Column out of range.")
            continue

        # Place checker
        for row in range(BOARD_ROWS - 1, -1, -1):
            if board[row][col] == " ":
                board[row][col] = current_player
                break
        else:
            print("Column is full. Please try again.")
            continue

        # Check for win
        if check_win(board, current_player):
            os.system('clear')
            print_board(board)
            print(f"Player {current_player} won!")
            break

        # Check for draw
        if check_draw(board):
            os.system('clear')
            print_board(board)
            print("It's a draw!")
            break

        # Switch player
        current_player_index = (current_player_index + 1) % num_players
        current_player = players[current_player_index]

play_game()
