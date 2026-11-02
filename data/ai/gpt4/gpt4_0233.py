import os
import random

# Constants
ROWS = 6
COLS = 7
MAX_PLAYERS = 5
CHECKERS = ["X", "O", "V", "H", "M"]

# Function to clear the screen
def clear_screen():
    os.system('clear')

# Function to create an empty board
def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

# Function to print the board
def print_board(board):
    print("  " + "   ".join([chr(65 + i) for i in range(COLS)]))
    print("+---" * COLS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLS + "+")

# Function to check if a column is valid and not full
def is_valid_column(board, col):
    return 0 <= col < COLS and board[0][col] == " "

# Function to drop a checker into a column
def drop_checker(board, col, checker):
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            break

# Function to check for any win condition
def check_win(board, checker):
    # Horizontal check
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True

    # Vertical check
    for row in range(ROWS - 3):
        for col in range(COLS):
            if all(board[row + i][col] == checker for i in range(4)):
                return True

    # Diagonal (bottom-left to top-right) check
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True

    # Diagonal (top-left to bottom-right) check
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True

    return False

# Function to check if the board is full
def is_draw(board):
    return all(board[0][col] != " " for col in range(COLS))

# Main game logic
def play_game():
    # Initialize game variables
    board = create_board(ROWS, COLS)
    num_players = 2  # Fixed to 2 players for this assignment
    players = CHECKERS[:num_players]
    
    # Randomly choose the first player
    current_player = random.randint(0, num_players - 1)

    # Main game loop
    while True:
        clear_screen()
        print_board(board)

        # Prompt the current player for a move
        print(f"Player {players[current_player]}'s turn")
        col_letter = input("Please enter a column (A-G): ").strip().upper()

        # Validate input
        if len(col_letter) != 1 or not col_letter.isalpha() or ord(col_letter) - 65 < 0 or ord(col_letter) - 65 >= COLS:
            print("Invalid input. Please enter a valid column letter.")
            input("Press Enter to continue...")
            continue

        col = ord(col_letter) - 65

        if not is_valid_column(board, col):
            print("This column is full or invalid. Please choose another column.")
            input("Press Enter to continue...")
            continue

        # Place the checker
        drop_checker(board, col, players[current_player])

        # Check for win
        if check_win(board, players[current_player]):
            clear_screen()
            print_board(board)
            print(f"Player {players[current_player]} won!")
            break

        # Check for draw
        if is_draw(board):
            clear_screen()
            print_board(board)
            print("The game is a draw!")
            break

        # Switch to the next player
        current_player = (current_player + 1) % num_players

# Run the game
if __name__ == "__main__":
    play_game()
