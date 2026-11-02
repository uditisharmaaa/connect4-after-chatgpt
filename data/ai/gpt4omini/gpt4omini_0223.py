import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    """Create and return a 2D board initialized with whitespace."""
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    """Clear the screen and print the current state of the board."""
    os.system('clear' if os.name != 'nt' else 'cls')  # Clear screen
    print("  " + "   ".join(chr(65 + i) for i in range(COLUMNS)))  # Column labels A-G
    print("+---+" + "---+" * (COLUMNS - 1))
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---+" + "---+" * (COLUMNS - 1))

def get_valid_input(player):
    """Prompt the player until a valid column input is received."""
    while True:
        column = input(f"Player {player}, please enter a column: ").upper()        
        if len(column) == 1 and 'A' <= column <= chr(65 + COLUMNS - 1):
            column_index = ord(column) - 65
            return column_index
        else:
            print("Invalid input. Please enter a letter from A to " + chr(65 + COLUMNS - 1))

def place_checker(board, column, player):
    """Place the player's checker in the specified column if valid."""
    for row in range(ROWS - 1, -1, -1):  # Start from the bottom of the column
        if board[row][column] == ' ':
            board[row][column] = player
            return True
    return False  # Indicates column is full

def check_winner(board, player):
    """Check for a win condition in the board."""
    # Check horizontal, vertical and diagonal (both) for 4 in a row
    # Horizontal
    for r in range(ROWS):
        for c in range(COLUMNS - 3):
            if all(board[r][c + i] == player for i in range(4)):
                return True

    # Vertical
    for c in range(COLUMNS):
        for r in range(ROWS - 3):
            if all(board[r + i][c] == player for i in range(4)):
                return True

    # Diagonal (top-left to bottom-right)
    for r in range(ROWS - 3):
        for c in range(COLUMNS - 3):
            if all(board[r + i][c + i] == player for i in range(4)):
                return True

    # Diagonal (top-right to bottom-left)
    for r in range(ROWS - 3):
        for c in range(3, COLUMNS):
            if all(board[r + i][c - i] == player for i in range(4)):
                return True

    return False

def check_draw(board):
    """Check if the board is full."""
    return all(board[0][c] != ' ' for c in range(COLUMNS))  # Check if top row is full

def main():
    board = create_board()
    current_player_index = random.randint(0, len(PLAYERS) - 1)
    game_over = False

    print_board(board)

    while not game_over:
        current_player = PLAYERS[current_player_index]
        
        # Get valid input and attempt to place checker
        column = get_valid_input(current_player)
        
        if place_checker(board, column, current_player):
            print_board(board)

            if check_winner(board, current_player):
                print(f"Player {current_player} won!")
                game_over = True
            
            elif check_draw(board):
                print("The game is a draw!")
                game_over = True
            
            # Switch to next player
            current_player_index = (current_player_index + 1) % len(PLAYERS)
        else:
            print(f"Column {chr(65 + column)} is full. Try again.")

if __name__ == "__main__":
    main()
