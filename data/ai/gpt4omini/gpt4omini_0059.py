import os
import random

# Constants for the game
NUM_ROWS = 6
NUM_COLUMNS = 7
MAX_COLUMNS = 26
PLAYERS = ['X', 'O', 'V', 'H', 'M']

def initialize_board():
    """Create and return an empty game board."""
    return [[' ' for _ in range(NUM_COLUMNS)] for _ in range(NUM_ROWS)]

def print_board(board):
    """Print the current state of the game board."""
    os.system('clear')  # Clear the console screen
    print("  " + "   ".join(chr(65 + i) for i in range(NUM_COLUMNS)))  # Column labels A-G
    print("+" + "---+" * NUM_COLUMNS)  # Top border
    for row in board:
        print("| " + " | ".join(row) + " |")  # Row content
        print("+" + "---+" * NUM_COLUMNS)  # Row border

def get_column_choice(player):
    """Prompt the player to choose a column, validating input."""
    while True:
        choice = input(f"Player {player}, please enter a column: ").upper()
        if len(choice) == 1 and 'A' <= choice <= chr(65 + NUM_COLUMNS - 1):
            return ord(choice) - 65  # Convert character to column index
        print("Invalid input. Please choose a valid column (A to {}).".format(chr(65 + NUM_COLUMNS - 1)))

def place_checker(board, column, player):
    """Place the player's checker in the specified column."""
    for row in reversed(board):  # Start checking from the bottom row
        if row[column] == ' ':
            row[column] = player
            return True
    return False  # Column is full

def check_win(board, player):
    """Check if the specified player has won the game."""
    def check_direction(dx, dy):
        count = 0
        for x in range(NUM_COLUMNS):
            for y in range(NUM_ROWS):
                if (0 <= x + dx * count < NUM_COLUMNS) and (0 <= y + dy * count < NUM_ROWS):
                    if board[y][x] == player:
                        count += 1
                    else:
                        count = 0
                    if count == 4:
                        return True
        return False

    # Check horizontal, vertical, and both diagonal directions
    return (check_direction(1, 0) or  # Horizontal
            check_direction(0, 1) or  # Vertical
            check_direction(1, 1) or  # Diagonal \
            check_direction(1, -1))   # Diagonal /

def is_draw(board):
    """Check if the game is a draw (board filled)."""
    return all(cell != ' ' for row in board for cell in row)

def main():
    """Main game loop."""
    board = initialize_board()
    players_count = len(PLAYERS)
    current_player_index = random.randint(0, players_count - 1)
    
    print_board(board)
    
    while True:
        current_player = PLAYERS[current_player_index]
        column = get_column_choice(current_player)
        
        if place_checker(board, column, current_player):
            print_board(board)
            if check_win(board, current_player):
                print(f"Player {current_player} won!")
                break
            if is_draw(board):
                print("The game is a draw!")
                break

            current_player_index = (current_player_index + 1) % players_count
        else:
            print("Column is full! Please try again.")

if __name__ == "__main__":
    main()
