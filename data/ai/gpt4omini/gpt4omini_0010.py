import random
import os

# Constants for board dimensions and player symbols
ROWS = 6
COLUMNS = 7
PLAYERS = ['X', 'O', 'V', 'H', 'M']  # Up to 5 players

def create_board():
    """Creates a game board initialized with spaces."""
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    """Prints the current state of the board."""
    os.system('clear')  # Clears the terminal screen
    print("  " + "   ".join(chr(i) for i in range(65, 65 + COLUMNS)))  # Column labels A, B, C, ...
    print("+---" + "+---" * (COLUMNS - 1) + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" + "+---" * (COLUMNS - 1) + "+")

def is_valid_input(column_input):
    """Checks if the input for the column is valid."""
    return column_input in range(COLUMNS)

def get_player_input(player):
    """Prompts the player to choose a column until valid input is received."""
    while True:
        try:
            column_input = input(f"Player {player}, please enter a column (A-{chr(65 + COLUMNS - 1)}): ").upper()
            if column_input < 'A' or column_input > chr(65 + COLUMNS - 1):
                raise ValueError
            column_index = ord(column_input) - 65
            if not is_valid_input(column_index):
                print("Invalid column. Try again.")
                continue
            return column_index
        except ValueError:
            print("Invalid input. Please enter a letter corresponding to a column.")

def drop_checker(board, column_index, checker):
    """Places the checker on the board and returns True if successful."""
    for row in reversed(board):  # Start from the bottom row
        if row[column_index] == " ":
            row[column_index] = checker
            return True
    return False  # Return False if the column is full

def check_winner(board, checker):
    """Checks if the specified checker has won."""
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True

    # Check vertical
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == checker for i in range(4)):
                return True

    # Check diagonal (bottom left to top right)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True

    # Check diagonal (top left to bottom right)
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True

    return False  # No winner found

def is_draw(board):
    """Checks if the game is a draw (all spots are filled)."""
    return all(cell != " " for row in board for cell in row)

def main():
    """Main function to run the Connect 4 game."""
    board = create_board()
    num_players = len(PLAYERS)
    current_player_index = random.randint(0, num_players - 1)

    print_board(board)
    
    while True:
        current_player = PLAYERS[current_player_index]
        column_index = get_player_input(current_player)

        if drop_checker(board, column_index, current_player):
            print_board(board)
            if check_winner(board, current_player):
                print(f"Player {current_player} won!")
                break
            if is_draw(board):
                print("The game is a draw!")
                break
            
            current_player_index = (current_player_index + 1) % num_players  # Switch player
        else:
            print("Column is full. Turn lost.")

if __name__ == "__main__":
    main()
