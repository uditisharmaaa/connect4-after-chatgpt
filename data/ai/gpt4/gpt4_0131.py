import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]  # Supports up to 5 players

# Create the board
def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

# Print the board
def print_board(board):
    os.system('clear')  # Clear the screen
    print("  " + "   ".join(chr(65 + c) for c in range(len(board[0]))))
    print("+---" * len(board[0]) + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * len(board[0]) + "+")

# Get the next available row in a column
def get_next_open_row(board, col):
    for row in range(len(board) - 1, -1, -1):
        if board[row][col] == " ":
            return row
    return -1

# Check for a win
def check_win(board, player):
    # Check horizontal
    for row in range(len(board)):
        for col in range(len(board[0]) - 3):
            if all(board[row][col + i] == player for i in range(4)):
                return True

    # Check vertical
    for col in range(len(board[0])):
        for row in range(len(board) - 3):
            if all(board[row + i][col] == player for i in range(4)):
                return True

    # Check diagonal (bottom-left to top-right)
    for row in range(len(board) - 3):
        for col in range(len(board[0]) - 3):
            if all(board[row + i][col + i] == player for i in range(4)):
                return True

    # Check diagonal (top-left to bottom-right)
    for row in range(3, len(board)):
        for col in range(len(board[0]) - 3):
            if all(board[row - i][col + i] == player for i in range(4)):
                return True

    return False

# Check for a draw
def check_draw(board):
    return all(board[0][col] != " " for col in range(len(board[0])))

# Validate user input
def validate_input(input_col, board):
    if len(input_col) != 1 or not input_col.isalpha():
        return False
    col = ord(input_col.upper()) - 65
    if col < 0 or col >= len(board[0]) or board[0][col] != " ":
        return False
    return True

# Main game logic
def play_game(rows, cols, num_players):
    board = create_board(rows, cols)
    players = CHECKERS[:num_players]
    current_player_idx = random.randint(0, num_players - 1)

    print_board(board)
    print(f"Player {players[current_player_idx]} starts the game!")

    while True:
        current_player = players[current_player_idx]
        valid_move = False

        while not valid_move:
            user_input = input(f"Player {current_player}, please enter a column: ").strip()
            if validate_input(user_input, board):
                col = ord(user_input.upper()) - 65
                row = get_next_open_row(board, col)
                if row != -1:  # Valid move
                    board[row][col] = current_player
                    valid_move = True
                else:
                    print("Column is full, try another column.")
            else:
                print("Invalid input, please try again.")

        print_board(board)

        # Check for win or draw
        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            break
        elif check_draw(board):
            print("The game is a draw!")
            break

        # Switch to the next player
        current_player_idx = (current_player_idx + 1) % num_players

# Run the game
if __name__ == "__main__":
    play_game(ROWS, COLS, NUM_PLAYERS)
