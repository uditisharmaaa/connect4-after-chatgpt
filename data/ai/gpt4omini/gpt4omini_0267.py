import os
import random

# Constants for the game dimensions and players
ROWS = 6
COLS = 7
MAX_COLUMNS = 26
PLAYERS = ['X', 'O', 'V', 'H', 'M']  # 5 players max

def create_board():
    """Initialize the game board with empty spaces."""
    return [[" "] * COLS for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the board."""
    os.system('clear')  # Clear the terminal screen
    print("  " + "   ".join(chr(65 + col) for col in range(COLS)))  # Column headers
    print("+" + "---+" * COLS)  # Top border
    
    for row in board:
        print("| " + " | ".join(row) + " |")  # Row content
        print("+" + "---+" * COLS)  # Border after each row

def is_valid_input(column_input):
    """Check if the input is a valid column selection."""
    return (len(column_input) == 1 and 
            'A' <= column_input <= chr(65 + COLS - 1))

def get_column_index(column_input):
    """Convert column letter to index."""
    return ord(column_input) - 65

def place_checker(board, column, checker):
    """Place the checker in the specified column."""
    for row in reversed(range(ROWS)):
        if board[row][column] == " ":
            board[row][column] = checker
            return True
    return False

def check_win(board, player):
    """Check for a win condition."""
    # Check horizontal, vertical and diagonal directions
    for row in range(ROWS):
        for col in range(COLS):
            if (check_direction(board, row, col, player, 1, 0) or  # horizontal
                check_direction(board, row, col, player, 0, 1) or  # vertical
                check_direction(board, row, col, player, 1, 1) or  # diagonal /
                check_direction(board, row, col, player, 1, -1):   # diagonal \
                return True
    return False

def check_direction(board, row, col, player, delta_row, delta_col):
    """Check in a specific direction for four in a row."""
    count = 0
    for step in range(4):
        r = row + step * delta_row
        c = col + step * delta_col
        if 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == player:
            count += 1
        else:
            break
    return count == 4

def check_draw(board):
    """Check if the board is full (i.e., draw condition)."""
    return all(board[0][col] != " " for col in range(COLS))

def main():
    """Main function to run the Connect 4 game."""
    board = create_board()
    current_player_index = random.randint(0, len(PLAYERS) - 1)
    game_over = False

    while not game_over:
        current_player = PLAYERS[current_player_index]
        print_board(board)
        column_input = input(f"Player {current_player}, please enter a column (A-{chr(65 + COLS - 1)}): ").upper()

        # Validate input
        while not is_valid_input(column_input):
            column_input = input("Invalid input. Please enter a valid column (A-{0}): ".format(chr(65 + COLS - 1))).upper()
        
        column_index = get_column_index(column_input)

        # Attempt to place the checker
        if place_checker(board, column_index, current_player):
            if check_win(board, current_player):
                print_board(board)
                print(f"Player {current_player} won!")
                game_over = True
            elif check_draw(board):
                print_board(board)
                print("The game is a draw!")
                game_over = True
            else:
                # Switch to the next player
                current_player_index = (current_player_index + 1) % len(PLAYERS)
        else:
            print(f"Column {column_input} is full. Try again.")

if __name__ == "__main__":
    main()
