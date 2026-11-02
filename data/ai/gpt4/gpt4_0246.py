import os
import random

# Constants
ROWS = 6
COLS = 7
MAX_PLAYERS = 5
PLAYERS = ['X', 'O', 'V', 'H', 'M'][:2]  # Set number of players to 2
EMPTY_CELL = " "

# Function to initialize the board
def initialize_board(rows, cols):
    return [[EMPTY_CELL for _ in range(cols)] for _ in range(rows)]

# Function to print the board
def print_board(board):
    os.system('clear')  # Clear the terminal
    header = "  " + "   ".join(chr(65 + col) for col in range(COLS))
    print(header)
    print("+---" * COLS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLS + "+")

# Function to validate the input and return column index
def get_valid_player_input(board, player):
    while True:
        choice = input(f"Player {player}, please enter a column: ").upper()
        if len(choice) != 1 or not choice.isalpha():
            print("Invalid input. Please enter a valid column letter.")
            continue

        col = ord(choice) - 65
        if col < 0 or col >= COLS:
            print("Column out of range. Try again.")
            continue

        if board[0][col] != EMPTY_CELL:
            print("Column is full. Choose a different one.")
            continue

        return col

# Function to place a checker on the board
def place_checker(board, col, player):
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == EMPTY_CELL:
            board[row][col] = player
            return row, col

# Function to check for a win at a specific position
def check_win(board, row, col, player):
    def count_consecutive(row, col, delta_row, delta_col):
        count = 0
        while 0 <= row < ROWS and 0 <= col < COLS and board[row][col] == player:
            count += 1
            row += delta_row
            col += delta_col
        return count

    # Check all directions
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]  # Horizontal, vertical, diagonal /
    for dr, dc in directions:
        total = (count_consecutive(row, col, dr, dc) +
                 count_consecutive(row, col, -dr, -dc) - 1)  # Subtract 1 to avoid double counting
        if total >= 4:
            return True
    return False

# Function to check for a draw
def check_draw(board):
    return all(board[0][col] != EMPTY_CELL for col in range(COLS))

# Main function to play the game
def play_game():
    board = initialize_board(ROWS, COLS)
    current_player_index = random.randint(0, len(PLAYERS) - 1)
    print_board(board)

    while True:
        player = PLAYERS[current_player_index]
        col = get_valid_player_input(board, player)
        row, col = place_checker(board, col, player)
        print_board(board)

        if check_win(board, row, col, player):
            print(f"Player {player} won!")
            break

        if check_draw(board):
            print("It's a draw!")
            break

        # Switch to the next player
        current_player_index = (current_player_index + 1) % len(PLAYERS)

# Run the game
if __name__ == "__main__":
    play_game()
