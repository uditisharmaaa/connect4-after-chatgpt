import os
import random

# Constants for the game
ROWS = 6
COLS = 7
MAX_PLAYERS = 5
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]

def create_board():
    """Create the initial game board."""
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the game board."""
    os.system('clear')  # clear the screen
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))
    print("+---" * COLS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLS + "+")

def is_valid_column(column, board):
    """Check if the column is valid for a move."""
    if column < 0 or column >= COLS:
        return False
    return board[0][column] == " "

def drop_checker(board, column, checker):
    """Place the checker in the selected column."""
    for row in reversed(board):
        if row[column] == " ":
            row[column] = checker
            return True
    return False

def check_winner(board, checker):
    """Check for a winner."""
    # Check horizontal
    for row in board:
        for col in range(COLS - 3):
            if row[col:col + 4] == [checker] * 4:
                return True

    # Check vertical
    for col in range(COLS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == checker for i in range(4)):
                return True

    # Check diagonal (down-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True

    # Check diagonal (up-right)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True

    return False

def is_draw(board):
    """Check if the board is full."""
    return all(cell != " " for row in board for cell in row)

def get_player_input(player, board):
    """Get and validate the player's input."""
    while True:
        move = input(f"Player {player}, please enter a column: ").strip().upper()
        if len(move) != 1 or not 'A' <= move <= chr(65 + COLS - 1):
            print("Invalid input. Please enter a valid column letter.")
            continue
        
        column = ord(move) - 65
        if not is_valid_column(column, board):
            print("Column is full or invalid. Please choose another column.")
            continue
        
        return column

def main():
    # Initialize the board
    board = create_board()
    players = PLAYER_CHECKERS[:2]  # Default to 2 players for submission
    current_player_idx = random.randint(0, len(players) - 1)

    # Start the game
    print_board(board)
    while True:
        current_player = players[current_player_idx]
        
        # Prompt player for a move
        column = get_player_input(current_player, board)
        
        # Place the checker
        drop_checker(board, column, current_player)
        
        # Print the updated board
        print_board(board)
        
        # Check for a win or draw
        if check_winner(board, current_player):
            print(f"Player {current_player} won!")
            break
        elif is_draw(board):
            print("The game is a draw!")
            break
        
        # Switch to the next player
        current_player_idx = (current_player_idx + 1) % len(players)

if __name__ == "__main__":
    main()
