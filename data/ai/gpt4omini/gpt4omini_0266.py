import os
import random

# Constants for the game configuration
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O', 'V', 'H', 'M']  # Up to 5 players

def create_board():
    """Create the game board initialized with spaces."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the Connect 4 board."""
    os.system('clear')  # Clear the screen
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))  # Column labels A-G
    print("+" + "---+" * COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)

def get_player_input(player):
    """Get a valid column input from the player."""
    while True:
        choice = input(f"Player {player}, please enter a column (A-G): ").upper()
        if len(choice) != 1 or choice < 'A' or choice >= chr(65 + COLS):
            print("Invalid input. Please enter a column letter from A to G.")
        else:
            return ord(choice) - 65  # Convert column letter to index

def drop_checker(board, col, checker):
    """Drop a checker into the specified column on the board."""
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = checker
            return True
    return False  # Column is full

def check_winner(board, checker):
    """Check for a winning condition for the specified checker."""
    # Check horizontal
    for row in board:
        for col in range(COLS - 3):
            if row[col] == checker and row[col + 1] == checker and row[col + 2] == checker and row[col + 3] == checker:
                return True
    # Check vertical
    for col in range(COLS):
        for row in range(ROWS - 3):
            if board[row][col] == checker and board[row + 1][col] == checker and board[row + 2][col] == checker and board[row + 3][col] == checker:
                return True
    # Check diagonal (/\)
    for col in range(COLS - 3):
        for row in range(3, ROWS):
            if board[row][col] == checker and board[row - 1][col + 1] == checker and board[row - 2][col + 2] == checker and board[row - 3][col + 3] == checker:
                return True
    # Check diagonal (\/)
    for col in range(COLS - 3):
        for row in range(ROWS - 3):
            if board[row][col] == checker and board[row + 1][col + 1] == checker and board[row + 2][col + 2] == checker and board[row + 3][col + 3] == checker:
                return True
    return False

def check_draw(board):
    """Check if the game is a draw (all spaces filled)."""
    return all(cell != ' ' for row in board for cell in row)

def main():
    """Main function to run the game."""
    board = create_board()
    current_player_index = random.randint(0, len(PLAYERS) - 1)  # Randomly choose starting player
    total_players = len(PLAYERS)

    print_board(board)

    while True:
        current_player = PLAYERS[current_player_index]
        col = get_player_input(current_player)
        
        # Try to drop the checker in the selected column
        if drop_checker(board, col, current_player):
            print_board(board)  # Print the updated board

            # Check for a win
            if check_winner(board, current_player):
                print(f"Player {current_player} won!")
                break

            # Check for a draw
            if check_draw(board):
                print("The game is a draw!")
                break

            # Move to the next player
            current_player_index = (current_player_index + 1) % total_players
        else:
            print("Column is full, please choose another column.")

if __name__ == "__main__":
    main()
