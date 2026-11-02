import os
import random

# Constants
COLUMNS = 7
ROWS = 6
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_LENGTH = 4

# Global variables
board = []
current_player = 0
players = []


def initialize_board():
    """Initialize the board with empty spaces."""
    global board
    board = [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]


def get_players():
    """Get the list of player checkers based on the number of players."""
    return CHECKERS[:NUM_PLAYERS]


def print_board():
    """Print the current state of the board."""
    os.system('clear')
    
    # Print column headers
    print("  ", end="")
    for col in range(COLUMNS):
        print(chr(ord('A') + col), end="   ")
    print()
    
    # Print top border
    print("+---" * COLUMNS + "+")
    
    # Print each row
    for row in range(ROWS):
        print("|", end="")
        for col in range(COLUMNS):
            print(" " + board[row][col] + " |", end="")
        print()
        print("+---" * COLUMNS + "+")


def is_valid_column(col_letter):
    """Check if the column letter is valid."""
    if len(col_letter) != 1:
        return False
    if not col_letter.isalpha():
        return False
    col_index = ord(col_letter.upper()) - ord('A')
    if col_index < 0 or col_index >= COLUMNS:
        return False
    return True


def get_drop_row(col_index):
    """Get the row where a checker should be placed in the given column.
    Returns -1 if the column is full."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_index] == " ":
            return row
    return -1


def place_checker(col_letter, player_checker):
    """Place a checker in the specified column.
    Returns True if successful, False otherwise."""
    col_index = ord(col_letter.upper()) - ord('A')
    drop_row = get_drop_row(col_index)
    
    if drop_row == -1:
        return False
    
    board[drop_row][col_index] = player_checker
    return True


def check_direction(row, col, player_checker, row_delta, col_delta):
    """Check if there are 4 checkers in a row in the given direction."""
    count = 0
    r = row
    c = col
    
    while r >= 0 and r < ROWS and c >= 0 and c < COLUMNS:
        if board[r][c] == player_checker:
            count += 1
            if count == WIN_LENGTH:
                return True
        else:
            break
        r += row_delta
        c += col_delta
    
    return False


def check_all_directions(row, col, player_checker):
    """Check if a player has won at the given position."""
    directions = [
        (0, 1),   # Horizontal right
        (1, 0),   # Vertical down
        (1, 1),   # Diagonal down-right
        (1, -1)   # Diagonal down-left
    ]
    
    for row_delta, col_delta in directions:
        # Check in positive direction
        if check_direction(row, col, player_checker, row_delta, col_delta):
            return True
        # Check in negative direction
        if check_direction(row, col, player_checker, -row_delta, -col_delta):
            return True
    
    return False


def check_win(row, col, player_checker):
    """Check if the last move resulted in a win."""
    return check_all_directions(row, col, player_checker)


def is_board_full():
    """Check if the board is completely full."""
    for row in range(ROWS):
        for col in range(COLUMNS):
            if board[row][col] == " ":
                return False
    return True


def get_valid_column_input(player_checker):
    """Get a valid column input from the player."""
    while True:
        user_input = input(f"Player {player_checker}, please enter a column: ")
        
        if not is_valid_column(user_input):
            print("Invalid input. Please enter a valid column letter (A-" + 
                  chr(ord('A') + COLUMNS - 1) + ").")
            continue
        
        col_index = ord(user_input.upper()) - ord('A')
        if get_drop_row(col_index) == -1:
            print("That column is full. Please enter a different column.")
            continue
        
        return user_input.upper()


def play_game():
    """Main game loop."""
    global current_player
    
    initialize_board()
    players_list = get_players()
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    print_board()
    
    while True:
        player_checker = players_list[current_player]
        col_letter = get_valid_column_input(player_checker)
        col_index = ord(col_letter) - ord('A')
        
        drop_row = get_drop_row(col_index)
        place_checker(col_letter, player_checker)
        
        print_board()
        
        if check_win(drop_row, col_index, player_checker):
            print(f"Player {player_checker} won!")
            return
        
        if is_board_full():
            print("It's a draw!")
            return
        
        current_player = (current_player + 1) % NUM_PLAYERS


if __name__ == "__main__":
    play_game()
