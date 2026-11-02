import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2  # Number of players (2-5)
CHECKERS = ['X', 'O', 'V', 'H', 'M']  # Checkers for up to 5 players

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')

def create_board(rows, columns):
    """Creates an empty Connect 4 board."""
    return [[' ' for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    """Prints the Connect 4 board."""
    # Print column labels
    labels = ' '.join(f' {chr(65 + i)} ' for i in range(len(board[0])))
    print(f"  {labels}")
    # Print rows with borders
    for row in board:
        print('+---' * len(row) + '+')
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
    print('+---' * len(board[0]) + '+')

def get_next_empty_row(board, column):
    """Finds the next available row in a column."""
    for row in range(len(board) - 1, -1, -1):
        if board[row][column] == ' ':
            return row
    return -1  # Column is full

def is_valid_column(column, board):
    """Checks if the column is valid and not full."""
    return 0 <= column < len(board[0]) and board[0][column] == ' '

def check_winner(board, player):
    """Checks for a winner (4 in a row horizontally, vertically, or diagonally)."""
    rows, cols = len(board), len(board[0])
    
    # Check horizontal
    for r in range(rows):
        for c in range(cols - 3):
            if all(board[r][c + i] == player for i in range(4)):
                return True
    
    # Check vertical
    for c in range(cols):
        for r in range(rows - 3):
            if all(board[r + i][c] == player for i in range(4)):
                return True
    
    # Check diagonal (down-right)
    for r in range(rows - 3):
        for c in range(cols - 3):
            if all(board[r + i][c + i] == player for i in range(4)):
                return True
    
    # Check diagonal (down-left)
    for r in range(rows - 3):
        for c in range(3, cols):
            if all(board[r + i][c - i] == player for i in range(4)):
                return True

    return False

def is_draw(board):
    """Checks if the game is a draw (board is full)."""
    return all(board[0][c] != ' ' for c in range(len(board[0])))

def play_game():
    """Main function to run the Connect 4 game."""
    # Initialization
    random.seed()  # Initialize random number generator
    board = create_board(ROWS, COLUMNS)
    players = CHECKERS[:PLAYERS]
    current_player = random.choice(players)
    clear_screen()
    print_board(board)
    
    # Game Loop
    while True:
        print(f"Player {current_player}, please enter a column (A-{chr(65 + COLUMNS - 1)}):")
        while True:
            column_input = input().upper()
            if len(column_input) == 1 and 'A' <= column_input <= chr(65 + COLUMNS - 1):
                column = ord(column_input) - 65
                if is_valid_column(column, board):
                    break
                else:
                    print(f"Column {column_input} is full. Choose another column:")
            else:
                print(f"Invalid input. Enter a valid column (A-{chr(65 + COLUMNS - 1)}):")

        # Place the checker
        row = get_next_empty_row(board, column)
        board[row][column] = current_player

        # Clear the screen and print the updated board
        clear_screen()
        print_board(board)

        # Check for a win or draw
        if check_winner(board, current_player):
            print(f"Player {current_player} won!")
            break
        if is_draw(board):
            print("The game is a draw!")
            break

        # Switch to the next player
        current_index = players.index(current_player)
        current_player = players[(current_index + 1) % PLAYERS]

# Run the game
if __name__ == "__main__":
    play_game()
