import os
import random

# Constants for the game configuration
ROWS = 6
COLS = 7
MAX_PLAYERS = 5
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board(rows=ROWS, cols=COLS):
    """Create a new game board with the specified dimensions."""
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Clear the screen and print the current state of the board."""
    os.system('clear')
    col_labels = "  " + "   ".join([chr(i) for i in range(ord('A'), ord('A') + len(board[0]))])
    print(col_labels)
    print("+---" * len(board[0]) + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * len(board[0]) + "+")

def is_valid_column(board, col):
    """Check if the selected column is valid for a move."""
    return 0 <= col < len(board[0]) and board[0][col] == " "

def place_checker(board, col, checker):
    """Place a checker in the specified column."""
    for row in reversed(board):
        if row[col] == " ":
            row[col] = checker
            return

def check_winner(board, checker):
    """Check for a win condition for the specified checker."""
    def check_line(line):
        return line == [checker] * 4

    # Check horizontal, vertical, diagonal (both directions)
    for row in range(ROWS):
        for col in range(COLS):
            if col <= COLS - 4 and check_line([board[row][col+i] for i in range(4)]):
                return True
            if row <= ROWS - 4 and check_line([board[row+i][col] for i in range(4)]):
                return True
            if row <= ROWS - 4 and col <= COLS - 4 and check_line([board[row+i][col+i] for i in range(4)]):
                return True
            if row <= ROWS - 4 and col >= 3 and check_line([board[row+i][col-i] for i in range(4)]):
                return True
    return False

def is_draw(board):
    """Check if the game is a draw."""
    return all(cell != " " for row in board for cell in row)

def get_column_input():
    """Prompt the player for a column input and validate it."""
    while True:
        try:
            col_input = input("Choose a column (A-G): ").strip().upper()
            if len(col_input) != 1 or not ('A' <= col_input <= 'G'):
                raise ValueError
            return ord(col_input) - ord('A')
        except ValueError:
            print("Invalid input. Please choose a valid column between A and G.")

def connect_4():
    """Main function to start and run the Connect 4 game."""
    board = create_board()
    num_players = 2
    players = CHECKERS[:num_players]
    current_player = random.choice(players)

    while True:
        print_board(board)
        print(f"Player {current_player}, please enter a column:")
        
        col = get_column_input()
        if not is_valid_column(board, col):
            print("Column is full or invalid. Try again.")
            continue
        
        place_checker(board, col, current_player)
        
        if check_winner(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break
        if is_draw(board):
            print_board(board)
            print("The game is a draw!")
            break

        current_player = players[(players.index(current_player) + 1) % num_players]

if __name__ == "__main__":
    connect_4()
