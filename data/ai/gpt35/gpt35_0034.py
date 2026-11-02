import os
import random

# --- Constants ---
ROWS = 6               # Number of rows on the board
COLUMNS = 7            # Number of columns on the board (max 26)
PLAYERS = 2            # Number of players (2 to 5)

# Checkers for players in order
CHECKERS = ["X", "O", "V", "H", "M"]

# --- Functions ---

def clear_screen():
    """Clear the terminal screen."""
    os.system('clear')

def create_board(rows, columns):
    """Create and return a board initialized with spaces."""
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    """Print the board using the format described."""
    clear_screen()
    # Print column headers (A, B, C, ...)
    header = "  "
    for c in range(len(board[0])):
        header += "  " + chr(ord('A') + c) + " "
    print(header)
    
    # Print board rows
    for row in board:
        print("+---" * len(row) + "+")
        line = "|"
        for cell in row:
            line += " " + cell + " |"
        print(line)
    print("+---" * len(board[0]) + "+")

def get_valid_column_input(board, player):
    """
    Prompt the player to enter a column letter.
    Validate input: uppercase letter, within board columns.
    Returns the corresponding column index (int).
    """
    columns = len(board[0])
    valid_letters = [chr(ord('A') + i) for i in range(columns)]
    
    while True:
        answer = input(f"Player {player}, please enter a column: ").strip().upper()
        if len(answer) != 1 or answer not in valid_letters:
            # Invalid input (wrong length or char not in allowed range)
            continue
        col = ord(answer) - ord('A')
        return col

def place_checker(board, col, checker):
    """
    Place the checker in the chosen column at the lowest available row.
    If column is full, return False (turn lost).
    Otherwise place checker and return True.
    """
    for row in range(len(board)-1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    return False

def check_winner(board, checker):
    """
    Check if the player with 'checker' has 4 in a row horizontally,
    vertically, or diagonally.
    Returns True if player wins, else False.
    """
    rows = len(board)
    cols = len(board[0])
    
    # Check horizontal
    for r in range(rows):
        count = 0
        for c in range(cols):
            if board[r][c] == checker:
                count += 1
                if count == 4:
                    return True
            else:
                count = 0
    
    # Check vertical
    for c in range(cols):
        count = 0
        for r in range(rows):
            if board[r][c] == checker:
                count += 1
                if count == 4:
                    return True
            else:
                count = 0
                
    # Check diagonal (\)
    for r in range(rows - 3):
        for c in range(cols - 3):
            if (board[r][c] == checker and
                board[r+1][c+1] == checker and
                board[r+2][c+2] == checker and
                board[r+3][c+3] == checker):
                return True
                
    # Check diagonal (/)
    for r in range(3, rows):
        for c in range(cols - 3):
            if (board[r][c] == checker and
                board[r-1][c+1] == checker and
                board[r-2][c+2] == checker and
                board[r-3][c+3] == checker):
                return True
    
    return False

def board_full(board):
    """
    Check if the board is full (no empty spaces).
    Returns True if full, else False.
    """
    for row in board:
        if " " in row:
            return False
    return True

def select_starting_player(num_players):
    """
    Randomly select starting player index (0 to num_players-1).
    """
    return random.randint(0, num_players -1)

# --- Main program ---

def main():
    board = create_board(ROWS, COLUMNS)
    players = CHECKERS[:PLAYERS]
    
    # Random starting player
    current_player_index = select_starting_player(PLAYERS)
    
    print_board(board)

    # Game Loop
    while True:
        current_checker = players[current_player_index]
        
        # Get valid user input
        col = get_valid_column_input(board, current_checker)
        
        # Try to place checker
        placed = place_checker(board, col, current_checker)
        if not placed:
            # Column full -> turn lost
            # Just switch to next player
            current_player_index = (current_player_index + 1) % PLAYERS
            print_board(board)
            continue
        
        print_board(board)
        
        # Check win condition
        if check_winner(board, current_checker):
            print(f"Player {current_checker} won!")
            break
        
        # Check draw condition
        if board_full(board):
            print("Game is a draw!")
            break
        
        # Next player's turn
        current_player_index = (current_player_index + 1) % PLAYERS

if __name__ == "__main__":
    main()
