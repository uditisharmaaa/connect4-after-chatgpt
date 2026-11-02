import os
import random

# Constants for the game
ROWS = 6
COLUMNS = 7
COLUMNS_LABEL = ["A", "B", "C", "D", "E", "F", "G"]
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']  # Symbols for the players
NUMBER_OF_PLAYERS = 3  # Set the number of players (2 to 5)

def create_board():
    """Create a 6x7 board initialized with empty spaces."""
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    """Display the board."""
    os.system('clear')  # Clear the console
    print(" " + "   ".join(COLUMNS_LABEL))
    for row in board:
        print("| " + " | ".join(row) + " |")
    print("-" * (COLUMNS * 4 + 1))

def get_column_index(column_label):
    """Convert column label to a column index."""
    if column_label in COLUMNS_LABEL:
        return COLUMNS_LABEL.index(column_label)
    return -1

def drop_piece(board, column, symbol):
    """Drop a player's symbol into the board."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][column] == ' ':
            board[row][column] = symbol
            return True
    return False

def is_valid_column(choice):
    """Check if the column choice is valid."""
    return choice in COLUMNS_LABEL

def check_winner(board, symbol):
    """Check the board for a win condition."""
    # Check horizontal locations
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col + i] == symbol for i in range(4)):
                return True

    # Check vertical locations
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == symbol for i in range(4)):
                return True

    # Check positively sloped diagonals
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == symbol for i in range(4)):
                return True

    # Check negatively sloped diagonals
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row - i][col + i] == symbol for i in range(4)):
                return True

    return False

def check_draw(board):
    """Check if the board is full, resulting in a draw."""
    return all(board[0][col] != ' ' for col in range(COLUMNS))

def connect_four():
    """Main function to run the Connect 4 game."""
    board = create_board()
    current_player = random.randint(0, NUMBER_OF_PLAYERS - 1)  # Randomly select the first player

    while True:
        print_board(board)
        print(f"Player {PLAYER_SYMBOLS[current_player]}'s turn.")

        # Get and validate user input
        choice = input("Choose a column (A-G): ").upper()
        if not is_valid_column(choice):
            print("Invalid choice. Please select a column from A to G.")
            continue
        
        column = get_column_index(choice)
        if not drop_piece(board, column, PLAYER_SYMBOLS[current_player]):
            print("The column is full. Choose another column.")
            continue

        # Check for win or draw conditions
        if check_winner(board, PLAYER_SYMBOLS[current_player]):
            print_board(board)
            print(f"Player {PLAYER_SYMBOLS[current_player]} wins!")
            break
        elif check_draw(board):
            print_board(board)
            print("The game is a draw!")
            break

        # Switch to next player
        current_player = (current_player + 1) % NUMBER_OF_PLAYERS

# Run the game
connect_four()
