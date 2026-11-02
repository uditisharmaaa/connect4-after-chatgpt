import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_COLUMNS = 26
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')

def create_board(rows, columns):
    """Creates an empty game board."""
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    """Prints the game board."""
    clear_screen()
    # Print column headers
    headers = "   ".join(chr(ord('A') + i) for i in range(len(board[0])))
    print(f"  {headers}")
    # Print board with grid lines
    for row in board:
        print("+---" * len(row) + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * len(board[0]) + "+")

def is_valid_column(column, columns):
    """Checks if the column input is valid."""
    return column.isalpha() and 'A' <= column < chr(ord('A') + columns)

def get_column_index(column):
    """Converts column letter to index."""
    return ord(column) - ord('A')

def is_column_full(board, column_index):
    """Checks if a column is full."""
    return board[0][column_index] != " "

def place_checker(board, column_index, checker):
    """Places the checker in the chosen column."""
    for row in reversed(board):
        if row[column_index] == " ":
            row[column_index] = checker
            return

def check_win(board, rows, columns, player):
    """Checks if the current player has won."""
    checker = CHECKERS[player]
    
    # Check horizontal
    for r in range(rows):
        for c in range(columns - 3):
            if all(board[r][c + i] == checker for i in range(4)):
                return True
            
    # Check vertical
    for r in range(rows - 3):
        for c in range(columns):
            if all(board[r + i][c] == checker for i in range(4)):
                return True
            
    # Check diagonal (down-right)
    for r in range(rows - 3):
        for c in range(columns - 3):
            if all(board[r + i][c + i] == checker for i in range(4)):
                return True
            
    # Check diagonal (up-right)
    for r in range(3, rows):
        for c in range(columns - 3):
            if all(board[r - i][c + i] == checker for i in range(4)):
                return True
    
    return False

def is_board_full(board):
    """Checks if the board is full."""
    return all(cell != " " for row in board for cell in row)

def main():
    # Set up the game
    players = PLAYERS
    rows, columns = ROWS, COLUMNS
    board = create_board(rows, columns)

    # Randomly choose the starting player
    current_player = random.randint(0, players - 1)

    while True:
        print_board(board)
        print(f"Player {CHECKERS[current_player]}'s turn.")
        column = input("Please enter a column: ").upper()

        # Validate input
        if not is_valid_column(column, columns):
            print("Invalid column. Try again!")
            continue

        column_index = get_column_index(column)
        if is_column_full(board, column_index):
            print("Column is full. Try again!")
            continue

        # Place the checker
        place_checker(board, column_index, CHECKERS[current_player])

        # Check for a win
        if check_win(board, rows, columns, current_player):
            print_board(board)
            print(f"Player {CHECKERS[current_player]} wins!")
            break

        # Check for a draw
        if is_board_full(board):
            print_board(board)
            print("The game is a draw!")
            break

        # Switch to the next player
        current_player = (current_player + 1) % players

if __name__ == "__main__":
    main()
