import os
import random

# Global constants
BOARD_WIDTH = 7
BOARD_HEIGHT = 6
NUM_PLAYERS = 2
WIN_LENGTH = 4
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]


def create_board(width, height):
    """Create an empty board with given dimensions."""
    return [[" " for _ in range(width)] for _ in range(height)]


def print_board(board):
    """Print the board with column labels and formatting."""
    os.system('clear')
    width = len(board[0])
    
    # Print column labels
    print("  ", end="")
    for col in range(width):
        print(f" {chr(65 + col)} ", end=" ")
    print()
    
    # Print board with borders
    for row in board:
        print("+", end="")
        for cell in row:
            print(f"---+", end="")
        print()
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
    print("+", end="")
    for _ in row:
        print("---+", end="")
    print()


def is_valid_move(board, col):
    """Check if a move is valid (column exists and has space)."""
    width = len(board[0])
    if col < 0 or col >= width:
        return False
    return board[0][col] == " "


def place_checker(board, col, checker):
    """Place a checker in the specified column, return True if successful."""
    height = len(board)
    for row in range(height - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    return False


def check_win(board, checker):
    """Check if the given checker has won."""
    height = len(board)
    width = len(board[0])
    
    # Check horizontal
    for row in range(height):
        for col in range(width - WIN_LENGTH + 1):
            if all(board[row][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check vertical
    for col in range(width):
        for row in range(height - WIN_LENGTH + 1):
            if all(board[row + i][col] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal (top-left to bottom-right)
    for row in range(height - WIN_LENGTH + 1):
        for col in range(width - WIN_LENGTH + 1):
            if all(board[row + i][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal (top-right to bottom-left)
    for row in range(height - WIN_LENGTH + 1):
        for col in range(WIN_LENGTH - 1, width):
            if all(board[row + i][col - i] == checker for i in range(WIN_LENGTH)):
                return True
    
    return False


def is_board_full(board):
    """Check if the board is completely full."""
    return all(cell != " " for row in board for cell in row)


def get_player_move(board, player_name):
    """Get valid input from player."""
    width = len(board[0])
    while True:
        user_input = input(f"Player {player_name}, please enter a column: ").strip().upper()
        
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        
        if user_input < 'A' or user_input >= chr(ord('A') + width):
            print(f"Invalid column. Please enter a letter between A and {chr(ord('A') + width - 1)}.")
            continue
        
        col = ord(user_input) - ord('A')
        
        if not is_valid_move(board, col):
            print("Column is full. Please choose another column.")
            continue
        
        return col


def main():
    """Main game loop."""
    board = create_board(BOARD_WIDTH, BOARD_HEIGHT)
    checkers = PLAYER_CHECKERS[:NUM_PLAYERS]
    
    # Randomly select first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    print_board(board)
    
    while True:
        current_checker = checkers[current_player_index]
        
        # Get player move
        col = get_player_move(board, current_checker)
        place_checker(board, col, current_checker)
        print_board(board)
        
        # Check for win
        if check_win(board, current_checker):
            print(f"Player {current_checker} won!")
            break
        
        # Check for draw
        if is_board_full(board):
            print("It's a draw!")
            break
        
        # Switch to next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
