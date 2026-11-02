import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]

# Function to create an empty board
def create_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]

# Function to print the board
def print_board(board):
    os.system("clear")  # Clear the screen
    column_labels = "  " + "   ".join(chr(65 + i) for i in range(len(board[0])))  # A, B, C, ...
    print(column_labels)
    print("+---" * len(board[0]) + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * len(board[0]) + "+")

# Function to check if the input is valid
def is_valid_column(column, columns):
    return column.isalpha() and len(column) == 1 and ord(column.upper()) - 65 in range(columns)

# Function to drop a checker into a column
def drop_checker(board, column, symbol):
    col_index = ord(column.upper()) - 65
    for row in reversed(board):
        if row[col_index] == " ":
            row[col_index] = symbol
            return True
    return False  # Column is full

# Function to check for a win
def check_win(board, symbol, rows, columns):
    # Horizontal check
    for r in range(rows):
        for c in range(columns - 3):
            if all(board[r][c + i] == symbol for i in range(4)):
                return True
    
    # Vertical check
    for r in range(rows - 3):
        for c in range(columns):
            if all(board[r + i][c] == symbol for i in range(4)):
                return True

    # Diagonal (positive slope) check
    for r in range(rows - 3):
        for c in range(columns - 3):
            if all(board[r + i][c + i] == symbol for i in range(4)):
                return True

    # Diagonal (negative slope) check
    for r in range(3, rows):
        for c in range(columns - 3):
            if all(board[r - i][c + i] == symbol for i in range(4)):
                return True
    
    return False

# Function to check if the board is full (draw)
def is_draw(board):
    return all(cell != " " for row in board for cell in row)

# Main function
def main():
    # Game setup
    board = create_board(ROWS, COLUMNS)
    num_players = 2  # Set to 2 as per the assignment
    player_symbols = PLAYER_SYMBOLS[:num_players]
    current_player = random.randint(0, num_players - 1)  # Random start player
    
    # Game loop
    while True:
        print_board(board)
        print(f"Player {player_symbols[current_player]}'s turn.")
        column = input("Please enter a column: ").strip().upper()

        # Validate input
        if not is_valid_column(column, COLUMNS):
            print("Invalid input. Please enter a valid column (A-G).")
            continue

        # Place the checker
        if not drop_checker(board, column, player_symbols[current_player]):
            print("Column is full. Please choose another column.")
            continue

        # Check for a win
        if check_win(board, player_symbols[current_player], ROWS, COLUMNS):
            print_board(board)
            print(f"Player {player_symbols[current_player]} won!")
            break

        # Check for a draw
        if is_draw(board):
            print_board(board)
            print("It's a draw!")
            break

        # Switch to the next player
        current_player = (current_player + 1) % num_players

# Run the game
if __name__ == "__main__":
    main()
