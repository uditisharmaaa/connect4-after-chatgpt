import random
import os

# Constants for the board size and number of players
NUM_ROWS = 6
NUM_COLUMNS = 7
NUM_PLAYERS = 2

# Constants for player symbols
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]

# Initialize the board
def create_board():
    return [[" " for _ in range(NUM_COLUMNS)] for _ in range(NUM_ROWS)]

# Print the board
def print_board(board):
    os.system('clear')
    column_labels = "  ".join(chr(i) for i in range(ord('A'), ord('A') + NUM_COLUMNS))
    print(f"  {column_labels}")
    print("+---" * NUM_COLUMNS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * NUM_COLUMNS + "+")

# Validate the player input
def validate_input(input_str):
    return input_str.isalpha() and len(input_str) == 1 and 'A' <= input_str <= chr(ord('A') + NUM_COLUMNS - 1)

# Drop the checker into the column
def drop_checker(board, column, symbol):
    for row in reversed(board):
        if row[column] == " ":
            row[column] = symbol
            break
    else:
        return False  # if the column is full
    return True

# Check for a win
def check_for_win(board, symbol):
    # Horizontal, Vertical, and Diagonal (both directions)
    for row in range(NUM_ROWS):
        for col in range(NUM_COLUMNS):
            if (col + 3 < NUM_COLUMNS and all(board[row][c] == symbol for c in range(col, col + 4))) or \
               (row + 3 < NUM_ROWS and all(board[r][col] == symbol for r in range(row, row + 4))) or \
               (row + 3 < NUM_ROWS and col + 3 < NUM_COLUMNS and all(board[row + i][col + i] == symbol for i in range(4))) or \
               (row + 3 < NUM_ROWS and col - 3 >= 0 and all(board[row + i][col - i] == symbol for i in range(4))):
                return True
    return False

# Check for a draw
def check_for_draw(board):
    return all(cell != " " for row in board for cell in row)

# Main game loop
def play_game():
    board = create_board()
    current_player = random.choice(range(NUM_PLAYERS))
    print_board(board)

    while True:
        print(f"Player {PLAYER_SYMBOLS[current_player]}, please enter a column:")

        column_input = input().strip().upper()
        if validate_input(column_input):
            column_idx = ord(column_input) - ord('A')
            if drop_checker(board, column_idx, PLAYER_SYMBOLS[current_player]):
                print_board(board)

                if check_for_win(board, PLAYER_SYMBOLS[current_player]):
                    print(f"Player {PLAYER_SYMBOLS[current_player]} won!")
                    break

                if check_for_draw(board):
                    print("The game is a draw!")
                    break

                current_player = (current_player + 1) % NUM_PLAYERS
            else:
                print(f"Column {column_input} is full. Try another column.")
        else:
            print("Invalid input. Please enter a valid column letter.")

# Run the game
play_game()
