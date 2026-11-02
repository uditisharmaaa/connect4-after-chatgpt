import os
import random

# Constants
BOARD_WIDTH = 7
BOARD_HEIGHT = 6
NUM_PLAYERS = 2
WIN_LENGTH = 4
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]


def initialize_board():
    """Create and return an empty board."""
    return [[" " for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]


def print_board(board):
    """Display the current state of the board."""
    os.system('clear')
    
    # Print column headers
    print("  ", end="")
    for col in range(BOARD_WIDTH):
        print(f" {chr(65 + col)} ", end=" ")
    print()
    
    # Print board with rows
    for row in board:
        print("+---" * BOARD_WIDTH + "+")
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
    print("+---" * BOARD_WIDTH + "+")


def is_valid_move(board, col):
    """Check if a move to the given column is valid."""
    if col < 0 or col >= BOARD_WIDTH:
        return False
    if board[0][col] != " ":
        return False
    return True


def get_drop_row(board, col):
    """Find the lowest empty row in the given column."""
    for row in range(BOARD_HEIGHT - 1, -1, -1):
        if board[row][col] == " ":
            return row
    return -1


def make_move(board, col, player_checker):
    """Place a checker in the board at the specified column."""
    row = get_drop_row(board, col)
    if row != -1:
        board[row][col] = player_checker
        return True
    return False


def check_win(board, player_checker):
    """Check if the player has won."""
    # Check horizontal
    for row in range(BOARD_HEIGHT):
        for col in range(BOARD_WIDTH - WIN_LENGTH + 1):
            if all(board[row][col + i] == player_checker for i in range(WIN_LENGTH)):
                return True
    
    # Check vertical
    for col in range(BOARD_WIDTH):
        for row in range(BOARD_HEIGHT - WIN_LENGTH + 1):
            if all(board[row + i][col] == player_checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal (top-left to bottom-right)
    for row in range(BOARD_HEIGHT - WIN_LENGTH + 1):
        for col in range(BOARD_WIDTH - WIN_LENGTH + 1):
            if all(board[row + i][col + i] == player_checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal (top-right to bottom-left)
    for row in range(BOARD_HEIGHT - WIN_LENGTH + 1):
        for col in range(WIN_LENGTH - 1, BOARD_WIDTH):
            if all(board[row + i][col - i] == player_checker for i in range(WIN_LENGTH)):
                return True
    
    return False


def is_board_full(board):
    """Check if the board is full (draw condition)."""
    for row in board:
        if " " in row:
            return False
    return True


def get_player_input(player_num):
    """Get and validate player input."""
    while True:
        try:
            user_input = input(f"Player {PLAYER_CHECKERS[player_num]}, please enter a column: ").strip().upper()
            if len(user_input) != 1:
                print("Invalid input. Please enter a single column letter.")
                continue
            col = ord(user_input) - ord('A')
            if col < 0 or col >= BOARD_WIDTH:
                print(f"Invalid column. Please enter a letter between A and {chr(65 + BOARD_WIDTH - 1)}.")
                continue
            return col
        except (ValueError, IndexError):
            print("Invalid input. Please enter a valid column letter.")


def play_game():
    """Main game loop."""
    board = initialize_board()
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    print_board(board)
    
    while True:
        # Get valid move from current player
        while True:
            col = get_player_input(current_player)
            if is_valid_move(board, col):
                break
            print("Column is full. Please choose another column.")
        
        # Make the move
        player_checker = PLAYER_CHECKERS[current_player]
        make_move(board, col, player_checker)
        print_board(board)
        
        # Check for win
        if check_win(board, player_checker):
            print(f"Player {player_checker} won!")
            return
        
        # Check for draw
        if is_board_full(board):
            print("It's a draw!")
            return
        
        # Switch to next player
        current_player = (current_player + 1) % NUM_PLAYERS


if __name__ == "__main__":
    play_game()
