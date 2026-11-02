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
    """Initialize the board with empty spaces"""
    global board
    board = [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]


def initialize_players():
    """Initialize players with their checkers"""
    global players, current_player
    players = []
    for i in range(NUM_PLAYERS):
        players.append(CHECKERS[i])
    
    # Randomly select first player
    current_player = random.randint(0, NUM_PLAYERS - 1)


def print_board():
    """Print the board with column labels and borders"""
    os.system('clear')
    
    # Print column labels
    print("  ", end="")
    for col in range(COLUMNS):
        print(chr(ord('A') + col), end="   ")
    print()
    
    # Print board with borders
    for row in range(ROWS):
        # Print top border
        print("+---" * COLUMNS + "+")
        
        # Print row content
        print("|", end="")
        for col in range(COLUMNS):
            print(" " + board[row][col] + " |", end="")
        print()
    
    # Print bottom border
    print("+---" * COLUMNS + "+")


def get_column_from_input(user_input):
    """Convert user input to column index"""
    if len(user_input) != 1:
        return -1
    
    if not user_input.isalpha():
        return -1
    
    user_input = user_input.upper()
    col_index = ord(user_input) - ord('A')
    
    if col_index < 0 or col_index >= COLUMNS:
        return -1
    
    return col_index


def is_column_full(col):
    """Check if a column is full"""
    return board[0][col] != " "


def place_checker(col, player_checker):
    """Place checker in the lowest available row of the column"""
    # Find the lowest empty row in the column
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = player_checker
            return True
    
    return False


def get_player_move():
    """Get valid move from current player"""
    while True:
        user_input = input(f"Player {players[current_player]}, please enter a column: ")
        
        # Validate input
        col = get_column_from_input(user_input)
        
        if col == -1:
            print("Invalid input. Please enter a valid column letter (A-" + chr(ord('A') + COLUMNS - 1) + ").")
            continue
        
        # Check if column is full
        if is_column_full(col):
            print("Column is full. Please choose another column.")
            continue
        
        return col


def check_horizontal_win(row, col, player_checker):
    """Check if there's a win horizontally"""
    count = 0
    
    # Check to the left
    for c in range(col, -1, -1):
        if board[row][c] == player_checker:
            count += 1
        else:
            break
    
    # Check to the right (excluding the current cell to avoid double counting)
    for c in range(col + 1, COLUMNS):
        if board[row][c] == player_checker:
            count += 1
        else:
            break
    
    return count >= WIN_LENGTH


def check_vertical_win(row, col, player_checker):
    """Check if there's a win vertically"""
    count = 0
    
    # Check upward
    for r in range(row, -1, -1):
        if board[r][col] == player_checker:
            count += 1
        else:
            break
    
    # Check downward (excluding the current cell)
    for r in range(row + 1, ROWS):
        if board[r][col] == player_checker:
            count += 1
        else:
            break
    
    return count >= WIN_LENGTH


def check_diagonal_win_left_right(row, col, player_checker):
    """Check if there's a win diagonally (top-left to bottom-right)"""
    count = 0
    
    # Check up-left
    r, c = row, col
    while r >= 0 and c >= 0:
        if board[r][c] == player_checker:
            count += 1
        else:
            break
        r -= 1
        c -= 1
    
    # Check down-right (excluding the current cell)
    r, c = row + 1, col + 1
    while r < ROWS and c < COLUMNS:
        if board[r][c] == player_checker:
            count += 1
        else:
            break
        r += 1
        c += 1
    
    return count >= WIN_LENGTH


def check_diagonal_win_right_left(row, col, player_checker):
    """Check if there's a win diagonally (top-right to bottom-left)"""
    count = 0
    
    # Check up-right
    r, c = row, col
    while r >= 0 and c < COLUMNS:
        if board[r][c] == player_checker:
            count += 1
        else:
            break
        r -= 1
        c += 1
    
    # Check down-left (excluding the current cell)
    r, c = row + 1, col - 1
    while r < ROWS and c >= 0:
        if board[r][c] == player_checker:
            count += 1
        else:
            break
        r += 1
        c -= 1
    
    return count >= WIN_LENGTH


def check_win(row, col, player_checker):
    """Check if the current move results in a win"""
    if check_horizontal_win(row, col, player_checker):
        return True
    
    if check_vertical_win(row, col, player_checker):
        return True
    
    if check_diagonal_win_left_right(row, col, player_checker):
        return True
    
    if check_diagonal_win_right_left(row, col, player_checker):
        return True
    
    return False


def find_row_for_checker(col):
    """Find the row where a checker would be placed in a column"""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            return row
    return -1


def is_board_full():
    """Check if the board is full"""
    for row in range(ROWS):
        for col in range(COLUMNS):
            if board[row][col] == " ":
                return False
    return True


def next_player():
    """Move to the next player"""
    global current_player
    current_player = (current_player + 1) % NUM_PLAYERS


def play_game():
    """Main game loop"""
    initialize_board()
    initialize_players()
    
    print_board()
    
    game_over = False
    
    while not game_over:
        # Get player move
        col = get_player_move()
        
        # Find row and place checker
        row = find_row_for_checker(col)
        player_checker = players[current_player]
        place_checker(col, player_checker)
        
        # Print board
        print_board()
        
        # Check for win
        if check_win(row, col, player_checker):
            print(f"Player {player_checker} won!")
            game_over = True
        # Check for draw
        elif is_board_full():
            print("It's a draw!")
            game_over = True
        else:
            # Move to next player
            next_player()


def main():
    """Main function"""
    play_game()


if __name__ == "__main__":
    main()
