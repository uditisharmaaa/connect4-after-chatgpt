import os
import random

# Constants
ROWS = 6
COLS = 7
MAX_PLAYERS = 5
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]
CLEAR_SCREEN = 'clear'

# Create the board
def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

# Clear the screen
def clear_screen():
    os.system(CLEAR_SCREEN)

# Print the board
def print_board(board):
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))
    print("+" + "---+" * COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)

# Check if input is valid
def is_valid_move(column, board):
    if column < 0 or column >= COLS:
        return False
    return board[0][column] == " "

# Place a checker
def drop_checker(board, column, symbol):
    for row in reversed(range(ROWS)):
        if board[row][column] == " ":
            board[row][column] = symbol
            return True
    return False

# Check for a win
def check_win(board, symbol):
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col + i] == symbol for i in range(4)):
                return True

    # Check vertical
    for row in range(ROWS - 3):
        for col in range(COLS):
            if all(board[row + i][col] == symbol for i in range(4)):
                return True

    # Check diagonal (bottom-left to top-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == symbol for i in range(4)):
                return True

    # Check diagonal (top-left to bottom-right)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i][col + i] == symbol for i in range(4)):
                return True

    return False

# Check for a draw
def check_draw(board):
    return all(board[0][col] != " " for col in range(COLS))

# Main game loop
def play_game():
    # Initialize board and players
    board = create_board()
    num_players = 2  # Adjustable up to MAX_PLAYERS, if required
    symbols = PLAYER_SYMBOLS[:num_players]
    current_player = random.randint(0, num_players - 1)

    clear_screen()
    print_board(board)

    while True:
        print(f"Player {symbols[current_player]}'s turn.")
        column_input = input("Please enter a column: ").upper()

        # Validate input
        if len(column_input) != 1 or not column_input.isalpha():
            print("Invalid input. Please enter a valid column letter.")
            continue

        column = ord(column_input) - ord('A')
        if not is_valid_move(column, board):
            print("Invalid move. Please select a valid column.")
            continue

        # Place the checker
        drop_checker(board, column, symbols[current_player])

        clear_screen()
        print_board(board)

        # Check for win or draw
        if check_win(board, symbols[current_player]):
            print(f"Player {symbols[current_player]} won!")
            break
        if check_draw(board):
            print("The game is a draw!")
            break

        # Switch to the next player
        current_player = (current_player + 1) % num_players

# Run the game
if __name__ == "__main__":
    play_game()
