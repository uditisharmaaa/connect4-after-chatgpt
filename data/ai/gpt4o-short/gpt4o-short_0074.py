import os
import random

# Constants defining the board size and player tokens
ROWS = 6
COLUMNS = 7
PLAYERS = ['X', 'O', 'V', 'H', 'M']

# The board will be represented as a 2D list (list of lists)
board = [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board():
    """Print the current state of the board."""
    os.system('clear')  # Clear the console for a fresh board display
    print("Current Board:")
    # Display column labels
    print(" A B C D E F G")
    # Display each row of the board
    for row in board:
        print(' '.join(row))

def validate_input(input_str):
    """Validate the player's input to ensure it is one of the columns A-G."""
    return input_str.upper() in [chr(i) for i in range(ord('A'), ord('A') + COLUMNS)]

def drop_piece(column, player):
    """Drop a piece in the desired column for the current player."""
    col_index = ord(column.upper()) - ord('A')
    for row in reversed(board):  # Start from the bottom of the board
        if row[col_index] == ' ':
            row[col_index] = player
            return True
    return False  # Column is full, piece cannot be placed

def check_win():
    """Check all possible win conditions (horizontal, vertical, diagonal)."""
    # Check horizontal wins
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if board[row][col] != ' ' and all(board[row][col + i] == board[row][col] for i in range(4)):
                return True
    
    # Check vertical wins
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if board[row][col] != ' ' and all(board[row + i][col] == board[row][col] for i in range(4)):
                return True
    
    # Check diagonal wins (/ direction)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if board[row][col] != ' ' and all(board[row + i][col + i] == board[row][col] for i in range(4)):
                return True

    # Check diagonal wins (\ direction)
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if board[row][col] != ' ' and all(board[row - i][col + i] == board[row][col] for i in range(4)):
                return True

    return False

def check_draw():
    """Checks for a draw condition, which occurs if all board positions are filled."""
    return all(cell != ' ' for row in board for cell in row)

def main():
    """Main function to initialize and control the game flow."""
    num_players = int(input("Enter number of players (2-5): "))
    players = PLAYERS[:num_players]
    current_player_index = random.randint(0, num_players - 1)
    
    while True:
        print_board()
        current_player = players[current_player_index]
        print(f"Player {current_player}'s turn")
        column = input(f"Choose a column (A-G): ")

        if not validate_input(column):
            print("Invalid input! Please choose a column between A and G.")
            continue

        if not drop_piece(column, current_player):
            print("Column full! Choose a different column.")
            continue

        # Check for win condition
        if check_win():
            print_board()
            print(f"Player {current_player} wins!")
            break

        # Check for draw condition
        if check_draw():
            print_board()
            print("It's a draw!")
            break

        # Switch to the next player
        current_player_index = (current_player_index + 1) % num_players

# Run the game
if __name__ == "__main__":
    main()
