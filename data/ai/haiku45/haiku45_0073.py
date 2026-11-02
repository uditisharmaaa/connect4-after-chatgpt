import os
import random

# Constants
COLUMNS = 7
ROWS = 6
NUM_PLAYERS = 2
WIN_LENGTH = 4
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board():
    """Create and return an empty board with all spaces."""
    board = []
    for row in range(ROWS):
        new_row = []
        for col in range(COLUMNS):
            new_row.append(" ")
        board.append(new_row)
    return board

def print_board(board):
    """Print the board in the required format."""
    os.system('clear')
    
    # Print column headers
    print("  ", end="")
    for col in range(COLUMNS):
        letter = chr(ord('A') + col)
        print(f" {letter}  ", end="")
    print()
    
    # Print top border
    print("+", end="")
    for col in range(COLUMNS):
        print("---+", end="")
    print()
    
    # Print each row
    for row in range(ROWS):
        print("|", end="")
        for col in range(COLUMNS):
            print(f" {board[row][col]} |", end="")
        print()
        
        # Print border after each row
        print("+", end="")
        for col in range(COLUMNS):
            print("---+", end="")
        print()

def is_valid_column(column_letter):
    """Check if the column letter is valid."""
    if len(column_letter) != 1:
        return False
    if not column_letter.isalpha():
        return False
    
    column_index = ord(column_letter.upper()) - ord('A')
    if column_index < 0 or column_index >= COLUMNS:
        return False
    
    return True

def can_place_checker(board, column_index):
    """Check if a checker can be placed in the column."""
    # Check if the top cell of the column is empty
    if board[0][column_index] == " ":
        return True
    return False

def place_checker(board, column_index, checker):
    """Place a checker in the column and return the row where it was placed."""
    # Find the lowest empty space in the column
    for row in range(ROWS - 1, -1, -1):
        if board[row][column_index] == " ":
            board[row][column_index] = checker
            return row
    return -1

def check_win(board, row, col, checker):
    """Check if there is a win at the given position."""
    # Check horizontal
    count = 1
    # Check left
    c = col - 1
    while c >= 0 and board[row][c] == checker:
        count += 1
        c -= 1
    # Check right
    c = col + 1
    while c < COLUMNS and board[row][c] == checker:
        count += 1
        c += 1
    if count >= WIN_LENGTH:
        return True
    
    # Check vertical
    count = 1
    # Check up
    r = row - 1
    while r >= 0 and board[r][col] == checker:
        count += 1
        r -= 1
    # Check down
    r = row + 1
    while r < ROWS and board[r][col] == checker:
        count += 1
        r += 1
    if count >= WIN_LENGTH:
        return True
    
    # Check diagonal (top-left to bottom-right)
    count = 1
    # Check up-left
    r, c = row - 1, col - 1
    while r >= 0 and c >= 0 and board[r][c] == checker:
        count += 1
        r -= 1
        c -= 1
    # Check down-right
    r, c = row + 1, col + 1
    while r < ROWS and c < COLUMNS and board[r][c] == checker:
        count += 1
        r += 1
        c += 1
    if count >= WIN_LENGTH:
        return True
    
    # Check diagonal (top-right to bottom-left)
    count = 1
    # Check up-right
    r, c = row - 1, col + 1
    while r >= 0 and c < COLUMNS and board[r][c] == checker:
        count += 1
        r -= 1
        c += 1
    # Check down-left
    r, c = row + 1, col - 1
    while r < ROWS and c >= 0 and board[r][c] == checker:
        count += 1
        r += 1
        c -= 1
    if count >= WIN_LENGTH:
        return True
    
    return False

def is_board_full(board):
    """Check if the board is full (draw condition)."""
    for row in range(ROWS):
        for col in range(COLUMNS):
            if board[row][col] == " ":
                return False
    return True

def get_player_checker(player_index):
    """Return the checker symbol for the given player."""
    return CHECKERS[player_index]

def play_game():
    """Main game loop."""
    board = create_board()
    
    # Randomly select first player
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    game_over = False
    
    while not game_over:
        checker = get_player_checker(current_player)
        player_name = chr(ord('A') + current_player) if NUM_PLAYERS > 2 else checker
        
        # Get valid input from player
        valid_input = False
        while not valid_input:
            user_input = input(f"Player {checker}, please enter a column: ")
            
            if not is_valid_column(user_input):
                print("Invalid input. Please enter a valid column letter.")
                continue
            
            column_index = ord(user_input.upper()) - ord('A')
            
            if not can_place_checker(board, column_index):
                print("Column is full. Please choose another column.")
                continue
            
            valid_input = True
        
        # Place the checker
        row = place_checker(board, column_index, checker)
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_win(board, row, column_index, checker):
            print(f"Player {checker} won!")
            game_over = True
        # Check for draw
        elif is_board_full(board):
            print("It's a draw!")
            game_over = True
        else:
            # Move to next player
            current_player = (current_player + 1) % NUM_PLAYERS

def main():
    """Start the game."""
    play_game()

if __name__ == "__main__":
    main()
