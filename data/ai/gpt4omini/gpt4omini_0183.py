import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O', 'V', 'H', 'M']  # Up to 5 players

def create_board():
    """Creates a game board with the given number of rows and columns."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Prints the current state of the Connect 4 board."""
    os.system('clear')  # Clear the console
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))  # Column labels
    print("+---" + "+---" * (COLS - 1) + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" + "+---" * (COLS - 1) + "+")

def get_valid_column():
    """Prompts user for a valid column input and returns the column index."""
    while True:
        column = input("Enter a column (A-G): ").upper()
        if len(column) == 1 and column in "ABCDEFG":
            col_index = ord(column) - 65
            if col_index < COLS:
                return col_index
        print("Invalid input. Please enter a letter from A to G.")

def drop_checker(board, column, player):
    """Drops the player's checker into the specified column."""
    for row in reversed(board):
        if row[column] == ' ':
            row[column] = player
            return True
    return False

def check_winner(board, player):
    """Checks if the player has 4 checkers in a row (win conditions)."""
    # Horizontal check
    for row in board:
        for col in range(COLS - 3):
            if all(row[col + i] == player for i in range(4)):
                return True
                
    # Vertical check
    for col in range(COLS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == player for i in range(4)):
                return True
                
    # Diagonal check (\)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == player for i in range(4)):
                return True
                
    # Diagonal check (/)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i][col + i] == player for i in range(4)):
                return True

    return False

def check_draw(board):
    """Checks if the board is full (draw condition)."""
    return all(cell != ' ' for row in board for cell in row)

def main():
    board = create_board()
    players_count = 2  # Set to 2 players for submission
    current_player_index = random.randint(0, players_count - 1)
    
    print_board(board)
    while True:
        current_player = PLAYERS[current_player_index]
        print(f"Player {current_player}, it's your turn.")

        column = get_valid_column()
        while not drop_checker(board, column, current_player):
            print("Column is full! Choose another column.")
            column = get_valid_column()

        print_board(board)

        if check_winner(board, current_player):
            print(f"Player {current_player} won!")
            break
        if check_draw(board):
            print("It's a draw!")
            break

        current_player_index = (current_player_index + 1) % players_count

if __name__ == "__main__":
    main()
