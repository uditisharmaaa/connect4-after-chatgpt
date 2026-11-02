import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_COLUMNS = 26
NUM_PLAYERS = 2
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]  # Supports up to 5 players

def create_board(rows, columns):
    """Initialize the board as a list of lists filled with spaces."""
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    """Prints the board to the console."""
    os.system('clear')  # Clear the console screen before printing
    column_labels = "  ".join(chr(ord('A') + i) for i in range(len(board[0])))
    print("  " + column_labels)
    print("+---" * len(board[0]) + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * len(board[0]) + "+")

def is_valid_input(column, board):
    """Check if the input column is valid and has space available."""
    if column < 0 or column >= len(board[0]):
        return False
    return board[0][column] == " "

def place_checker(board, column, player_symbol):
    """Place the checker in the lowest available space in the chosen column."""
    for row in reversed(board):
        if row[column] == " ":
            row[column] = player_symbol
            break

def check_win(board, player_symbol):
    """Check all win conditions: horizontal, vertical, and diagonal."""
    # Horizontal check
    for row in board:
        for i in range(len(row) - 3):
            if row[i:i+4] == [player_symbol] * 4:
                return True

    # Vertical check
    for col in range(len(board[0])):
        for row in range(len(board) - 3):
            if all(board[row+i][col] == player_symbol for i in range(4)):
                return True

    # Diagonal checks
    for row in range(len(board) - 3):
        for col in range(len(board[0]) - 3):
            if all(board[row+i][col+i] == player_symbol for i in range(4)):
                return True
        for col in range(3, len(board[0])):
            if all(board[row+i][col-i] == player_symbol for i in range(4)):
                return True

    return False

def check_draw(board):
    """Check if the game is a draw (i.e., no more valid moves)."""
    return all(cell != " " for row in board for cell in row)

def main():
    # Initialize the game board
    board = create_board(ROWS, COLUMNS)

    # Randomly select the starting player
    current_player = random.randint(0, NUM_PLAYERS - 1)

    # Game loop
    while True:
        print_board(board)
        player_symbol = PLAYER_SYMBOLS[current_player]
        print(f"Player {player_symbol}, please enter a column:")
        
        while True:
            try:
                input_char = input().strip().upper()
                column_choice = ord(input_char) - ord('A')
                if len(input_char) == 1 and is_valid_input(column_choice, board):
                    break
                print("Invalid input. Please enter a valid column (A-G):")
            except:
                print("Invalid input. Please enter a valid column (A-G):")

        place_checker(board, column_choice, player_symbol)

        if check_win(board, player_symbol):
            print_board(board)
            print(f"Player {player_symbol} won!")
            break

        if check_draw(board):
            print_board(board)
            print("The game is a draw!")
            break

        # Switch to the next player
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
