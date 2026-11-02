import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']  # Checker symbols for up to 5 players

# Helper function to clear the screen
def clear_screen():
    os.system('clear')

# Initializes an empty board
def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

# Prints the board along with column labels
def print_board(board):
    col_labels = "  " + "   ".join([chr(65 + i) for i in range(len(board[0]))])
    print(col_labels)
    print("+" + "---+" * len(board[0]))
    for row in board:
        print("|" + "|".join(f" {cell} " for cell in row) + "|")
        print("+" + "---+" * len(board[0]))

# Check if the column choice is valid
def valid_column(choice, cols, board):
    if len(choice) != 1 or not choice.isalpha():
        return False
    column = ord(choice.upper()) - 65
    if column < 0 or column >= cols or board[0][column] != " ":
        return False
    return True

# Place the checker in the correct location
def place_checker(player, column, board):
    for row in range(len(board) - 1, -1, -1):
        if board[row][column] == " ":
            board[row][column] = CHECKERS[player]
            return

# Check for a possible win
def check_win(board, player):
    symbol = CHECKERS[player]

    # Check horizontal
    for row in board:
        for col in range(len(row) - 3):
            if row[col:col+4] == [symbol] * 4:
                return True

    # Check vertical
    for col in range(len(board[0])):
        for row in range(len(board) - 3):
            if all(board[row+i][col] == symbol for i in range(4)):
                return True

    # Check diagonal (down-right)
    for row in range(len(board) - 3):
        for col in range(len(board[0]) - 3):
            if all(board[row+i][col+i] == symbol for i in range(4)):
                return True

    # Check diagonal (down-left)
    for row in range(len(board) - 3):
        for col in range(3, len(board[0])):
            if all(board[row+i][col-i] == symbol for i in range(4)):
                return True

    return False

# Check if the board is full (draw)
def check_draw(board):
    return all(cell != " " for row in board for cell in row)

# Main game function
def connect_4():
    # Initialize the board
    board = create_board(ROWS, COLS)

    # Determine players and starting player
    current_player = random.randint(0, PLAYERS - 1)
    
    # Game loop
    while True:
        clear_screen()
        print_board(board)
        print(f"Player {CHECKERS[current_player]}'s turn.")
        
        # Get user input
        while True:
            column_input = input("Please enter a column letter: ").strip().upper()
            if valid_column(column_input, COLS, board):
                break
            print("Invalid column. Try again.")

        # Place the checker
        column = ord(column_input) - 65
        place_checker(current_player, column, board)

        # Check for a win
        if check_win(board, current_player):
            clear_screen()
            print_board(board)
            print(f"Player {CHECKERS[current_player]} won!")
            break

        # Check for a draw
        if check_draw(board):
            clear_screen()
            print_board(board)
            print("It's a draw!")
            break

        # Move to the next player
        current_player = (current_player + 1) % PLAYERS

# Run the game
if __name__ == "__main__":
    connect_4()
