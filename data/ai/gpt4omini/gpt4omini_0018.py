import os
import random

# Constants for game dimensions and number of players
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O', 'V', 'H', 'M']  # Players' checkers

def create_board():
    """Creates a game board initialized with whitespace."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Prints the current game board."""
    # Clear the console before printing the board
    os.system('clear')
    
    # Print column labels
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))
    print("+" + "---+" * COLS)
    
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)

def get_first_player():
    """Randomly chooses the first player."""
    return random.choice(PLAYERS[:2])  # Choose between first two players

def is_valid_input(col_input):
    """Validates user input for column selection."""
    if len(col_input) != 1 or not col_input.isalpha():
        return False
    col = ord(col_input.upper()) - 65
    return 0 <= col < COLS

def drop_checker(board, col, checker):
    """Drops a checker into the specified column on the board."""
    for row in reversed(range(ROWS)):
        if board[row][col] == ' ':
            board[row][col] = checker
            return row  # Return the row where the checker was placed
    return -1  # Column is full

def check_win(board):
    """Checks for a win condition in the board."""
    # Check horizontal, vertical, and diagonal for a winning condition
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] != ' ':
                if (check_direction(board, r, c, 1, 0) or  # Horizontal
                    check_direction(board, r, c, 0, 1) or  # Vertical
                    check_direction(board, r, c, 1, 1) or  # Diagonal /
                    check_direction(board, r, c, 1, -1)):  # Diagonal \
                    return True
    return False

def check_direction(board, row, col, delta_row, delta_col):
    """Check for 4 in a line in a specific direction."""
    player = board[row][col]
    count = 0
    
    for i in range(4):
        r = row + i * delta_row
        c = col + i * delta_col
        if 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == player:
            count += 1
        else:
            break
    
    return count == 4

def check_draw(board):
    """Checks if the board is full and the game is a draw."""
    return all(cell != ' ' for row in board for cell in row)

def main():
    """Main game loop for Connect 4."""
    board = create_board()
    current_player_index = PLAYERS.index(get_first_player())
    
    while True:
        print_board(board)
        current_player = PLAYERS[current_player_index]
        col_input = input(f"Player {current_player}, please enter a column: ").upper()
        
        # Validate input
        while not is_valid_input(col_input):
            col_input = input("Invalid input. Please enter a valid column: ").upper()
        
        col = ord(col_input) - 65
        
        # Place the checker
        if drop_checker(board, col, current_player) == -1:
            print("Column is full. Try another column.")
            continue
        
        # Check for win
        if check_win(board):
            print_board(board)
            print(f"Player {current_player} won!")
            break
        
        # Check for draw
        if check_draw(board):
            print_board(board)
            print("The game is a draw!")
            break
        
        # Switch player
        current_player_index = (current_player_index + 1) % len(PLAYERS)

if __name__ == "__main__":
    main()
