import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]


def initialize_board(rows, cols):
    """Initialize the game board with empty spaces."""
    board = []
    for i in range(rows):
        row = []
        for j in range(cols):
            row.append(" ")
        board.append(row)
    return board


def print_board(board, cols):
    """Print the current state of the board."""
    os.system('clear')
    
    # Print column headers
    print("  ", end="")
    for col in range(cols):
        letter = chr(ord('A') + col)
        print(f" {letter}  ", end="")
    print()
    
    # Print board with borders
    for row in board:
        # Print top border
        print("+---" * cols + "+")
        
        # Print row content
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
    
    # Print bottom border
    print("+---" * cols + "+")


def get_column_input(cols):
    """Get valid column input from the player."""
    while True:
        user_input = input("Please enter a column: ").strip().upper()
        
        # Check if input is a single letter
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        
        # Check if input is a letter
        if not user_input.isalpha():
            print("Invalid input. Please enter a letter.")
            continue
        
        # Convert letter to column index
        col_index = ord(user_input) - ord('A')
        
        # Check if column index is within bounds
        if col_index < 0 or col_index >= cols:
            print(f"Invalid input. Please enter a letter between A and {chr(ord('A') + cols - 1)}.")
            continue
        
        return col_index


def place_checker(board, col, player_symbol, rows, cols):
    """Place a checker in the specified column. Returns True if successful."""
    # Find the lowest empty row in the column
    for row in range(rows - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = player_symbol
            return True
    
    # Column is full
    print("This column is full. Please choose another column.")
    return False


def check_horizontal_win(board, rows, cols, player_symbol):
    """Check if the player has won horizontally."""
    for row in range(rows):
        for col in range(cols - WIN_LENGTH + 1):
            if all(board[row][col + i] == player_symbol for i in range(WIN_LENGTH)):
                return True
    return False


def check_vertical_win(board, rows, cols, player_symbol):
    """Check if the player has won vertically."""
    for col in range(cols):
        for row in range(rows - WIN_LENGTH + 1):
            if all(board[row + i][col] == player_symbol for i in range(WIN_LENGTH)):
                return True
    return False


def check_diagonal_win(board, rows, cols, player_symbol):
    """Check if the player has won diagonally."""
    # Check diagonal going down-right
    for row in range(rows - WIN_LENGTH + 1):
        for col in range(cols - WIN_LENGTH + 1):
            if all(board[row + i][col + i] == player_symbol for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal going down-left
    for row in range(rows - WIN_LENGTH + 1):
        for col in range(WIN_LENGTH - 1, cols):
            if all(board[row + i][col - i] == player_symbol for i in range(WIN_LENGTH)):
                return True
    
    return False


def check_win(board, rows, cols, player_symbol):
    """Check if the player has won the game."""
    return (check_horizontal_win(board, rows, cols, player_symbol) or
            check_vertical_win(board, rows, cols, player_symbol) or
            check_diagonal_win(board, rows, cols, player_symbol))


def check_draw(board, rows, cols):
    """Check if the board is full (draw)."""
    for row in range(rows):
        for col in range(cols):
            if board[row][col] == " ":
                return False
    return True


def play_game(rows, cols, num_players):
    """Main game loop."""
    # Initialize the board
    board = initialize_board(rows, cols)
    
    # Get player symbols
    players = PLAYER_SYMBOLS[:num_players]
    
    # Randomly select first player
    current_player_index = random.randint(0, num_players - 1)
    
    # Print the initial board
    print_board(board, cols)
    
    # Game loop
    while True:
        # Get current player symbol
        current_player_symbol = players[current_player_index]
        
        # Get player input
        print(f"Player {current_player_symbol}, ", end="")
        col = get_column_input(cols)
        
        # Try to place the checker
        if place_checker(board, col, current_player_symbol, rows, cols):
            # Print the updated board
            print_board(board, cols)
            
            # Check for win
            if check_win(board, rows, cols, current_player_symbol):
                print(f"Player {current_player_symbol} won!")
                break
            
            # Check for draw
            if check_draw(board, rows, cols):
                print("It's a draw!")
                break
            
            # Move to next player
            current_player_index = (current_player_index + 1) % num_players
        else:
            # Invalid move, print board and ask again
            print_board(board, cols)


def main():
    """Main function to run the Connect 4 game."""
    play_game(ROWS, COLS, NUM_PLAYERS)


if __name__ == "__main__":
    main()
