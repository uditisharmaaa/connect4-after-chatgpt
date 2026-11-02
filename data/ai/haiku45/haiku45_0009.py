import os
import random

# Constants
COLUMNS = 7
ROWS = 6
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_LENGTH = 4

# Global board
board = []
current_player = 0
player_checkers = []


def initialize_board():
    """Initialize the board with empty spaces"""
    global board
    board = [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]


def initialize_players():
    """Initialize player checkers based on number of players"""
    global player_checkers, current_player
    player_checkers = CHECKERS[:PLAYERS]
    current_player = random.randint(0, PLAYERS - 1)


def clear_screen():
    """Clear the terminal screen"""
    os.system('clear')


def print_board():
    """Print the board in the required format"""
    # Print column headers
    print("  ", end="")
    for col in range(COLUMNS):
        print(chr(65 + col), end="   ")
    print()
    
    # Print board with borders
    for row in range(ROWS):
        # Print top border
        print("+", end="")
        for col in range(COLUMNS):
            print("---+", end="")
        print()
        
        # Print row content
        print("|", end="")
        for col in range(COLUMNS):
            print(" " + board[row][col] + " |", end="")
        print()
    
    # Print bottom border
    print("+", end="")
    for col in range(COLUMNS):
        print("---+", end="")
    print()


def get_column_input():
    """Get valid column input from player"""
    while True:
        column_input = input(f"Player {player_checkers[current_player]}, please enter a column: ").strip().upper()
        
        # Validate input
        if len(column_input) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        
        if not column_input.isalpha():
            print("Invalid input. Please enter a letter.")
            continue
        
        col_index = ord(column_input) - ord('A')
        
        if col_index < 0 or col_index >= COLUMNS:
            print(f"Invalid input. Please enter a letter between A and {chr(65 + COLUMNS - 1)}.")
            continue
        
        # Check if column is full
        if board[0][col_index] != " ":
            print("Column is full. Please choose another column.")
            continue
        
        return col_index


def place_checker(col_index):
    """Place checker in the specified column"""
    # Find the lowest empty row in the column
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = player_checkers[current_player]
            return True
    return False


def check_horizontal_win():
    """Check if current player has won horizontally"""
    current_checker = player_checkers[current_player]
    
    for row in range(ROWS):
        for col in range(COLUMNS - WIN_LENGTH + 1):
            if all(board[row][col + i] == current_checker for i in range(WIN_LENGTH)):
                return True
    return False


def check_vertical_win():
    """Check if current player has won vertically"""
    current_checker = player_checkers[current_player]
    
    for col in range(COLUMNS):
        for row in range(ROWS - WIN_LENGTH + 1):
            if all(board[row + i][col] == current_checker for i in range(WIN_LENGTH)):
                return True
    return False


def check_diagonal_win():
    """Check if current player has won diagonally"""
    current_checker = player_checkers[current_player]
    
    # Check diagonal going down-right
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(COLUMNS - WIN_LENGTH + 1):
            if all(board[row + i][col + i] == current_checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal going down-left
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(WIN_LENGTH - 1, COLUMNS):
            if all(board[row + i][col - i] == current_checker for i in range(WIN_LENGTH)):
                return True
    
    return False


def check_win():
    """Check if current player has won"""
    return check_horizontal_win() or check_vertical_win() or check_diagonal_win()


def check_draw():
    """Check if the board is full (draw)"""
    for col in range(COLUMNS):
        if board[0][col] == " ":
            return False
    return True


def next_player():
    """Move to the next player"""
    global current_player
    current_player = (current_player + 1) % PLAYERS


def play_game():
    """Main game loop"""
    clear_screen()
    print_board()
    
    while True:
        # Get player input
        col_index = get_column_input()
        
        # Place checker
        place_checker(col_index)
        
        # Clear screen and print updated board
        clear_screen()
        print_board()
        
        # Check for win
        if check_win():
            print(f"Player {player_checkers[current_player]} won!")
            break
        
        # Check for draw
        if check_draw():
            print("Draw!")
            break
        
        # Move to next player
        next_player()


def main():
    """Main function to start the game"""
    initialize_board()
    initialize_players()
    play_game()


if __name__ == "__main__":
    main()
