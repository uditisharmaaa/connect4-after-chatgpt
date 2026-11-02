import os
import random

# Constants for board dimensions and number of players
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5

# Checkers assigned to each player
CHECKERS = ["X", "O", "V", "H", "M"]

# Function to clear the screen
def clear_screen():
    os.system('clear')  # Use 'cls' if running on Windows

# Function to create and initialize the board
def create_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]

# Function to print the board
def print_board(board):
    clear_screen()
    column_labels = "   ".join(chr(65 + i) for i in range(len(board[0])))
    print(f"  {column_labels}")
    print("+---" * len(board[0]) + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * len(board[0]) + "+")

# Function to check if a column input is valid
def is_valid_column(input_col, board):
    if len(input_col) != 1 or not input_col.isalpha() or not input_col.isupper():
        return False
    col_idx = ord(input_col) - 65
    if col_idx < 0 or col_idx >= len(board[0]) or board[0][col_idx] != " ":
        return False
    return True

# Function to drop the checker into the board
def drop_checker(board, col, checker):
    col_idx = ord(col) - 65
    for row in range(len(board)-1, -1, -1):
        if board[row][col_idx] == " ":
            board[row][col_idx] = checker
            return row, col_idx

# Function to check if a player has won
def check_win(board, row, col, checker):
    def check_direction(delta_row, delta_col):
        count = 1
        for d in (-1, 1):  # Check in both directions
            r, c = row + d * delta_row, col + d * delta_col
            while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == checker:
                count += 1
                if count >= 4:  # 4 in a row detected
                    return True
                r += d * delta_row
                c += d * delta_col
        return False

    # Check all directions (horizontal, vertical, diagonal /, diagonal \)
    return (check_direction(0, 1) or   # Horizontal
            check_direction(1, 0) or   # Vertical
            check_direction(1, 1) or   # Diagonal \
            check_direction(1, -1))    # Diagonal /

# Function to check if the board is full (draw)
def check_draw(board):
    for col in range(len(board[0])):
        if board[0][col] == " ":
            return False
    return True

# Main game function
def play_game():
    # Initialize the board
    board = create_board(ROWS, COLUMNS)
    num_players = 2  # Set to 2 for this specific assignment
    players = CHECKERS[:num_players]

    # Randomly choose the starting player
    current_player_idx = random.randint(0, num_players - 1)

    # Main game loop
    while True:
        print_board(board)
        current_player = players[current_player_idx]
        print(f"Player {current_player}, please enter a column:")
        
        # Get valid column input from the player
        column_input = input().strip()
        while not is_valid_column(column_input, board):
            print("Invalid column. Please enter a valid column (A-G):")
            column_input = input().strip()

        # Drop the checker
        row, col = drop_checker(board, column_input, current_player)

        # Check for a win
        if check_win(board, row, col, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break

        # Check for a draw
        if check_draw(board):
            print_board(board)
            print("The game is a draw!")
            break

        # Switch to the next player
        current_player_idx = (current_player_idx + 1) % num_players

# Run the game
if __name__ == "__main__":
    play_game()
