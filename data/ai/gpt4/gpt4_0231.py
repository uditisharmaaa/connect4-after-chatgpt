import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]

def clear_screen():
    """Clears the screen."""
    os.system('clear')

def create_board(rows, columns):
    """Creates the game board."""
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    """Prints the game board."""
    clear_screen()
    column_labels = "  " + "   ".join(chr(65 + i) for i in range(len(board[0])))
    print(column_labels)
    print("+---" * len(board[0]) + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * len(board[0]) + "+")

def get_valid_column_input(board):
    """Gets a valid column input from the user."""
    while True:
        column = input("Please enter a column: ").upper()
        if len(column) == 1 and column.isalpha():
            col_index = ord(column) - 65
            if 0 <= col_index < len(board[0]):
                if board[0][col_index] == " ":
                    return col_index
                else:
                    print("Column is full. Try another.")
            else:
                print("Column is out of bounds. Try another.")
        else:
            print("Invalid input. Enter a valid column letter.")

def drop_checker(board, column, checker):
    """Drops the checker into the specified column."""
    for row in reversed(board):
        if row[column] == " ":
            row[column] = checker
            return

def check_winner(board, checker):
    """Checks if a player has won."""
    rows, cols = len(board), len(board[0])

    # Check horizontal
    for r in range(rows):
        for c in range(cols - 3):
            if all(board[r][c + i] == checker for i in range(4)):
                return True

    # Check vertical
    for r in range(rows - 3):
        for c in range(cols):
            if all(board[r + i][c] == checker for i in range(4)):
                return True

    # Check diagonal (down-right)
    for r in range(rows - 3):
        for c in range(cols - 3):
            if all(board[r + i][c + i] == checker for i in range(4)):
                return True

    # Check diagonal (up-right)
    for r in range(3, rows):
        for c in range(cols - 3):
            if all(board[r - i][c + i] == checker for i in range(4)):
                return True

    return False

def is_draw(board):
    """Checks if the game is a draw."""
    return all(cell != " " for row in board for cell in row)

def play_game():
    """Main function to play the game."""
    # Initialize game settings
    board = create_board(ROWS, COLUMNS)
    num_players = 2
    players = PLAYER_SYMBOLS[:num_players]
    random.shuffle(players)
    turn = 0

    # Game loop
    while True:
        print_board(board)
        current_player = players[turn % num_players]
        print(f"Player {current_player}, it's your turn!")
        
        column = get_valid_column_input(board)
        drop_checker(board, column, current_player)

        # Check for win or draw
        if check_winner(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break
        if is_draw(board):
            print_board(board)
            print("The game is a draw!")
            break

        turn += 1

# Run the game
if __name__ == "__main__":
    play_game()
