import os
import random

# Global constants
COLUMNS = 7
ROWS = 6
NUM_PLAYERS = 2
WIN_LENGTH = 4
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]


def initialize_board():
    """
    Initialize the board with all empty spaces.
    Returns a 2D list representing the board.
    """
    board = [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]
    return board


def print_board(board):
    """
    Print the current state of the board to the console.
    """
    os.system('clear')
    
    # Print column headers
    print("  ", end="")
    for col in range(COLUMNS):
        print(f"{chr(ord('A') + col):^3} ", end="")
    print()
    
    # Print board with borders
    for row in range(ROWS):
        # Top border
        print("+", end="")
        for col in range(COLUMNS):
            print("---+", end="")
        print()
        
        # Row content
        print("|", end="")
        for col in range(COLUMNS):
            print(f" {board[row][col]} |", end="")
        print()
    
    # Bottom border
    print("+", end="")
    for col in range(COLUMNS):
        print("---+", end="")
    print()


def is_valid_column(column_letter, board):
    """
    Check if the given column letter is valid and has space.
    Returns True if valid, False otherwise.
    """
    if len(column_letter) != 1:
        return False
    
    if not column_letter.isalpha():
        return False
    
    col_index = ord(column_letter.upper()) - ord('A')
    
    if col_index < 0 or col_index >= COLUMNS:
        return False
    
    if board[0][col_index] != " ":
        return False
    
    return True


def get_player_input(player_checker, board):
    """
    Get and validate the player's input for column choice.
    Returns the column index (0-based).
    """
    while True:
        user_input = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        
        if is_valid_column(user_input, board):
            return ord(user_input) - ord('A')
        else:
            print("Invalid input. Please enter a valid column letter (A-" + 
                  chr(ord('A') + COLUMNS - 1) + ") that is not full.")


def place_checker(board, col_index, player_checker):
    """
    Place the player's checker in the specified column.
    The checker falls to the lowest available row.
    Returns True if successful, False if column is full.
    """
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = player_checker
            return True
    
    return False


def check_direction(board, row, col, player_checker, row_delta, col_delta):
    """
    Check if there are 4 checkers in a row in the given direction.
    """
    count = 0
    current_row = row
    current_col = col
    
    while (0 <= current_row < ROWS and 
           0 <= current_col < COLUMNS and 
           board[current_row][current_col] == player_checker):
        count += 1
        current_row += row_delta
        current_col += col_delta
    
    return count


def check_win(board, row, col, player_checker):
    """
    Check if the player has won by getting 4 in a row.
    Checks horizontal, vertical, and diagonal directions.
    """
    # Directions: (vertical, horizontal, diagonal1, diagonal2)
    directions = [
        (1, 0),    # Vertical
        (0, 1),    # Horizontal
        (1, 1),    # Diagonal (top-left to bottom-right)
        (1, -1)    # Diagonal (top-right to bottom-left)
    ]
    
    for row_delta, col_delta in directions:
        # Count in positive direction
        positive_count = check_direction(board, row + row_delta, col + col_delta, 
                                        player_checker, row_delta, col_delta)
        # Count in negative direction
        negative_count = check_direction(board, row - row_delta, col - col_delta, 
                                        player_checker, -row_delta, -col_delta)
        # Total count includes the current piece
        total_count = positive_count + negative_count + 1
        
        if total_count >= WIN_LENGTH:
            return True
    
    return False


def is_board_full(board):
    """
    Check if the board is completely full (draw condition).
    """
    for row in range(ROWS):
        for col in range(COLUMNS):
            if board[row][col] == " ":
                return False
    
    return True


def get_next_player(current_player_index, num_players):
    """
    Get the next player's index.
    """
    return (current_player_index + 1) % num_players


def play_game():
    """
    Main game loop for Connect 4.
    """
    board = initialize_board()
    
    # Get player checkers based on number of players
    player_checkers = PLAYER_CHECKERS[:NUM_PLAYERS]
    
    # Randomly select the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    print_board(board)
    print(f"Player {player_checkers[current_player_index]} starts the game!")
    input("Press Enter to continue...")
    
    # Game loop
    while True:
        print_board(board)
        
        current_player_checker = player_checkers[current_player_index]
        
        # Get valid input from player
        col_index = get_player_input(current_player_checker, board)
        
        # Place the checker
        place_checker(board, col_index, current_player_checker)
        
        # Find the row where the checker was placed (for win checking)
        placed_row = -1
        for row in range(ROWS):
            if board[row][col_index] == current_player_checker:
                placed_row = row
                break
        
        # Check for win
        if check_win(board, placed_row, col_index, current_player_checker):
            print_board(board)
            print(f"Player {current_player_checker} won!")
            break
        
        # Check for draw
        if is_board_full(board):
            print_board(board)
            print("The game is a draw!")
            break
        
        # Move to next player
        current_player_index = get_next_player(current_player_index, NUM_PLAYERS)


if __name__ == "__main__":
    play_game()
