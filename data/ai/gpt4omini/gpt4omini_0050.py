import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O', 'V', 'H', 'M']  # Up to 5 players

def create_board():
    """Create a game board initialized with whitespaces."""
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Clear the screen and print the current state of the board."""
    os.system('clear')  # Clear the terminal screen
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))  # Column labels A, B, C, ...
    print("+" + "---+" * COLS)  # Print upper border
    for row in board:
        print("| " + " | ".join(row) + " |")  # Print each row
        print("+" + "---+" * COLS)  # Print row separator

def get_input(player):
    """Get a valid column input from the player."""
    while True:
        column = input(f"Player {player}, please enter a column: ").upper()  # Ask for column input
        if column in [chr(65 + i) for i in range(COLS)]:  # Check if valid column
            return ord(column) - 65
        else:
            print("Invalid input. Please enter a letter corresponding to a column (A-G).")

def place_checker(board, column, player):
    """Place a checker in the board at the given column."""
    for row in reversed(board):  # Start from the bottom of the column
        if row[column] == " ":
            row[column] = player  # Place checker if the space is empty
            return True
    return False  # Return False if the column is full

def check_win(board, player):
    """Check for a win condition for the player."""
    # Check horizontal, vertical, and diagonal wins
    for r in range(ROWS):
        for c in range(COLS):
            if (check_direction(board, r, c, player, 0, 1) or  # Horizontal
                check_direction(board, r, c, player, 1, 0) or  # Vertical
                check_direction(board, r, c, player, 1, 1) or  # Diagonal \
                check_direction(board, r, c, player, 1, -1)):  # Diagonal /
                return True
    return False

def check_direction(board, start_row, start_col, player, delta_row, delta_col):
    """Check if four in a row exists from a starting position in a specified direction."""
    for count in range(4):
        row = start_row + count * delta_row
        col = start_col + count * delta_col
        if (row < 0 or row >= ROWS or col < 0 or col >= COLS or board[row][col] != player):
            return False
    return True
  
def check_draw(board):
    """Check if the board is full and there are no winners."""
    return all(cell != " " for row in board for cell in row)

def main():
    """Main game function."""
    board = create_board()  # Initialize the game board
    current_player_index = random.randint(0, (len(PLAYERS) - 1))  # Randomly select first player
    total_players = len(PLAYERS)
  
    while True:
        print_board(board)  # Print board state
        current_player = PLAYERS[current_player_index]  # Get current player's symbol
        
        column = get_input(current_player)  # Get input from current player
        if not place_checker(board, column, current_player):  # Try to place the checker
            print("Column is full! Please choose another column.")
            continue  # Skip turn if the column was full

        if check_win(board, current_player):  # Check if the current player won
            print_board(board)  # Print final board
            print(f"Player {current_player} won!")  # Announce winner
            break

        if check_draw(board):  # Check if the board has drawn
            print_board(board)
            print("The game is a draw!")  # Announce draw
            break

        current_player_index = (current_player_index + 1) % total_players  # Switch turns

if __name__ == "__main__":
    main()  # Start the game
