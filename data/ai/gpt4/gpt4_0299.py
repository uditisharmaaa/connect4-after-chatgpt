import os
import random

# Constants for board dimensions and number of players
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]  # Checkers for up to 5 players

def create_board(rows, cols):
    """Create a board with the given dimensions."""
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Print the Connect 4 board."""
    os.system('clear')
    column_labels = "  " + "   ".join(chr(65 + i) for i in range(len(board[0])))
    divider = "+---" * len(board[0]) + "+"
    print(column_labels)
    print(divider)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print(divider)

def is_valid_column(column, board):
    """Check if the input column is valid."""
    return column.isalpha() and len(column) == 1 and "A" <= column < chr(65 + len(board[0]))

def is_column_full(column_index, board):
    """Check if a column is completely filled."""
    return board[0][column_index] != " "

def get_available_row(column, board):
    """Get the lowest available row in the given column."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][column] == " ":
            return row
    return None

def place_checker(column, player, board):
    """Place the current player's checker in the board."""
    column_index = ord(column) - 65
    row = get_available_row(column_index, board)
    if row is not None:
        board[row][column_index] = player
        return True
    return False

def check_winner(board, player):
    """Check if the given player has won."""
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if (board[row][col] == player and board[row][col + 1] == player and
                board[row][col + 2] == player and board[row][col + 3] == player):
                return True

    # Check vertical
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if (board[row][col] == player and board[row + 1][col] == player and
                board[row + 2][col] == player and board[row + 3][col] == player):
                return True

    # Check diagonal (bottom-left to top-right)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if (board[row][col] == player and board[row + 1][col + 1] == player and
                board[row + 2][col + 2] == player and board[row + 3][col + 3] == player):
                return True

    # Check diagonal (top-left to bottom-right)
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if (board[row][col] == player and board[row - 1][col + 1] == player and
                board[row - 2][col + 2] == player and board[row - 3][col + 3] == player):
                return True

    return False

def is_draw(board):
    """Check if the game is a draw."""
    return all(board[0][col] != " " for col in range(COLUMNS))

def main():
    # Setup
    board = create_board(ROWS, COLUMNS)
    current_player_index = random.randint(0, PLAYERS - 1)
    players = CHECKERS[:PLAYERS]
    print("Welcome to Connect 4!")
    print_board(board)

    # Main game loop
    while True:
        current_player = players[current_player_index]
        print(f"Player {current_player}, it's your turn.")
        
        # Handle input
        column = input("Please enter a column letter (A-G): ").upper()
        while (not is_valid_column(column, board) or 
               is_column_full(ord(column) - 65, board)):
            print("Invalid input. Try again.")
            column = input("Please enter a column letter (A-G): ").upper()
        
        # Place the checker and print board
        place_checker(column, current_player, board)
        print_board(board)

        # Check for winner or draw
        if check_winner(board, current_player):
            print(f"Player {current_player} won!")
            break
        if is_draw(board):
            print("It's a draw!")
            break
        
        # Switch to the next player
        current_player_index = (current_player_index + 1) % PLAYERS

if __name__ == "__main__":
    main()
