import os
import random

# Constants for board dimensions and number of players
ROWS = 6
COLUMNS = 7
PLAYER_COUNT = 2
CHECKERS = ["X", "O", "V", "H", "M"]  # Symbols for checkers (maximum 5 players)

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')

def create_board(rows, columns):
    """Initializes and returns an empty board."""
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    """Prints the board."""
    column_labels = "  " + "   ".join(chr(65 + i) for i in range(len(board[0])))
    divider = "+---" * len(board[0]) + "+"
    print(column_labels)
    for row in board:
        print(divider)
        print("| " + " | ".join(row) + " |")
    print(divider)

def get_column_index(column_input):
    """Converts a column letter input to an index."""
    return ord(column_input.upper()) - ord("A")

def is_valid_input(input_value, columns):
    """Checks if the player's input is valid."""
    return len(input_value) == 1 and input_value.isalpha() and "A" <= input_value.upper() < chr(65 + columns)

def is_column_full(board, column_index):
    """Checks if the selected column is full."""
    return board[0][column_index] != " "

def drop_checker(board, column_index, checker):
    """Drops the checker into the specified column."""
    for row in reversed(board):
        if row[column_index] == " ":
            row[column_index] = checker
            break

def check_winner(board, checker):
    """Checks if the player has won."""
    for r in range(len(board)):
        for c in range(len(board[0])):
            # Check horizontal
            if c + 3 < len(board[0]) and all(board[r][c + i] == checker for i in range(4)):
                return True
            # Check vertical
            if r + 3 < len(board) and all(board[r + i][c] == checker for i in range(4)):
                return True
            # Check diagonal right
            if r + 3 < len(board) and c + 3 < len(board[0]) and all(board[r + i][c + i] == checker for i in range(4)):
                return True
            # Check diagonal left
            if r + 3 < len(board) and c - 3 >= 0 and all(board[r + i][c - i] == checker for i in range(4)):
                return True
    return False

def check_draw(board):
    """Checks if the game is a draw."""
    return all(board[0][c] != " " for c in range(len(board[0])))

def main():
    """Main function to run the Connect 4 game."""
    # Initialize game
    board = create_board(ROWS, COLUMNS)
    players = [CHECKERS[i] for i in range(PLAYER_COUNT)]
    current_player = random.randint(0, PLAYER_COUNT - 1)  # Randomly select starting player

    while True:
        clear_screen()
        print_board(board)
        print(f"Player {players[current_player]}, it's your turn.")
        
        # Get valid input from player
        while True:
            column_input = input("Please enter a column: ")
            if is_valid_input(column_input, COLUMNS):
                column_index = get_column_index(column_input)
                if not is_column_full(board, column_index):
                    break
                else:
                    print("Column is full. Try another column.")
            else:
                print("Invalid input. Enter a valid column letter.")

        # Place the checker
        drop_checker(board, column_index, players[current_player])

        # Check for a win
        if check_winner(board, players[current_player]):
            clear_screen()
            print_board(board)
            print(f"Player {players[current_player]} won!")
            break

        # Check for a draw
        if check_draw(board):
            clear_screen()
            print_board(board)
            print("The game is a draw!")
            break

        # Switch to the next player
        current_player = (current_player + 1) % PLAYER_COUNT

if __name__ == "__main__":
    main()
