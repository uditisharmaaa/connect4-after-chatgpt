import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']  # Checker symbols for up to 5 players

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')

def create_board():
    """Creates the game board."""
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    """Prints the game board to the console."""
    clear_screen()
    # Print column labels
    print("  " + "   ".join(chr(65 + i) for i in range(COLUMNS)))
    print("+---" * COLUMNS + "+")
    # Print rows
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

def is_valid_column(column, board):
    """Checks if a column choice is valid (within bounds and not full)."""
    return 0 <= column < COLUMNS and board[0][column] == ' '

def get_lowest_row(column, board):
    """Finds the lowest empty row in a given column."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][column] == ' ':
            return row
    return -1

def check_winner(board, player):
    """Checks if the given player has won the game."""
    # Horizontal check
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col + i] == player for i in range(4)):
                return True
    # Vertical check
    for row in range(ROWS - 3):
        for col in range(COLUMNS):
            if all(board[row + i][col] == player for i in range(4)):
                return True
    # Diagonal (down-right) check
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == player for i in range(4)):
                return True
    # Diagonal (up-right) check
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row - i][col + i] == player for i in range(4)):
                return True
    return False

def check_draw(board):
    """Checks if the board is full and the game is a draw."""
    return all(board[0][col] != ' ' for col in range(COLUMNS))

def get_player_input(player, board):
    """Gets and validates input from the player."""
    while True:
        column_input = input(f"Player {player}, please enter a column: ").strip().upper()
        if len(column_input) == 1 and 'A' <= column_input <= chr(65 + COLUMNS - 1):  # Validating column letter
            column = ord(column_input) - 65
            if is_valid_column(column, board):
                return column
            else:
                print("The column is full! Please choose another one.")
        else:
            print("Invalid input! Please enter a valid column letter.")

def main():
    """Main function to run the Connect 4 game."""
    # Game setup
    random.seed()  # Initialize random seed
    board = create_board()
    player_symbols = CHECKERS[:PLAYERS]
    current_player_index = random.randint(0, PLAYERS - 1)
    
    print_board(board)
    print(f"Randomly selected Player {player_symbols[current_player_index]} to start.")

    while True:
        # Get current player's turn
        current_player = player_symbols[current_player_index]
        column = get_player_input(current_player, board)
        
        # Place the checker
        row = get_lowest_row(column, board)
        board[row][column] = current_player
        print_board(board)

        # Check for win or draw
        if check_winner(board, current_player):
            print(f"Player {current_player} won!")
            break
        if check_draw(board):
            print("The game is a draw!")
            break

        # Switch to the next player
        current_player_index = (current_player_index + 1) % PLAYERS

if __name__ == "__main__":
    main()
