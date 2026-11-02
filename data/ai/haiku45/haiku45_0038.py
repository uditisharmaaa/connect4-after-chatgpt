import os
import random

# Constants
BOARD_COLUMNS = 7
BOARD_ROWS = 6
NUM_PLAYERS = 2
WIN_LENGTH = 4
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]


def create_board(rows, cols):
    """Create an empty board with all spaces."""
    board = []
    for i in range(rows):
        row = []
        for j in range(cols):
            row.append(" ")
        board.append(row)
    return board


def print_board(board):
    """Print the board in the required format."""
    os.system('clear')
    
    rows = len(board)
    cols = len(board[0])
    
    # Print column headers
    print("  ", end="")
    for col in range(cols):
        print(chr(ord('A') + col), end="   ")
    print()
    
    # Print board with separators
    for row in range(rows):
        # Print top border
        print("+---" * cols + "+")
        
        # Print row content
        print("|", end="")
        for col in range(cols):
            print(" " + board[row][col] + " |", end="")
        print()
    
    # Print bottom border
    print("+---" * cols + "+")


def get_column_input(board):
    """Get and validate column input from the player."""
    cols = len(board[0])
    
    while True:
        user_input = input("Player " + current_player + ", please enter a column: ")
        
        # Check if input is a single character
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        
        # Check if input is a letter
        if not user_input.isalpha():
            print("Invalid input. Please enter a letter.")
            continue
        
        # Convert to uppercase and check if in range
        col_letter = user_input.upper()
        col_index = ord(col_letter) - ord('A')
        
        # Check if column is within board dimensions
        if col_index < 0 or col_index >= cols:
            print("Invalid input. Please enter a letter between A and " + chr(ord('A') + cols - 1) + ".")
            continue
        
        # Check if column is full
        if board[0][col_index] != " ":
            print("Column is full. Please choose another column.")
            continue
        
        return col_index


def place_checker(board, col, checker):
    """Place a checker in the specified column."""
    rows = len(board)
    
    # Find the lowest empty row in the column
    for row in range(rows - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    
    return False


def check_win(board, checker):
    """Check if the specified checker has won."""
    rows = len(board)
    cols = len(board[0])
    
    # Check horizontal
    for row in range(rows):
        for col in range(cols - WIN_LENGTH + 1):
            if all(board[row][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check vertical
    for row in range(rows - WIN_LENGTH + 1):
        for col in range(cols):
            if all(board[row + i][col] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal (top-left to bottom-right)
    for row in range(rows - WIN_LENGTH + 1):
        for col in range(cols - WIN_LENGTH + 1):
            if all(board[row + i][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal (top-right to bottom-left)
    for row in range(rows - WIN_LENGTH + 1):
        for col in range(WIN_LENGTH - 1, cols):
            if all(board[row + i][col - i] == checker for i in range(WIN_LENGTH)):
                return True
    
    return False


def check_draw(board):
    """Check if the board is full (draw)."""
    for cell in board[0]:
        if cell == " ":
            return False
    return True


def get_next_player(current_index, num_players):
    """Get the next player index."""
    return (current_index + 1) % num_players


# Main game loop
def main():
    global current_player
    
    # Create board
    board = create_board(BOARD_ROWS, BOARD_COLUMNS)
    
    # Create list of players
    players = []
    for i in range(NUM_PLAYERS):
        players.append(PLAYER_CHECKERS[i])
    
    # Randomly select first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    current_player = players[current_player_index]
    
    # Print initial board
    print_board(board)
    
    # Game loop
    game_over = False
    
    while not game_over:
        # Get player input
        col = get_column_input(board)
        
        # Place checker
        place_checker(board, col, current_player)
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_win(board, current_player):
            print("Player " + current_player + " won!")
            game_over = True
        
        # Check for draw
        elif check_draw(board):
            print("Draw!")
            game_over = True
        
        # Move to next player
        else:
            current_player_index = get_next_player(current_player_index, NUM_PLAYERS)
            current_player = players[current_player_index]


if __name__ == "__main__":
    main()
