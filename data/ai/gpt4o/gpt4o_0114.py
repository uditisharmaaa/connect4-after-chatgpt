import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
PLAYER_MARKERS = ["X", "O", "V", "H", "M"]

def clear_screen():
    """Clear the console screen."""
    os.system('clear')

def create_board(rows, columns):
    """Create a board with given dimensions."""
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    """Print the current state of the board."""
    clear_screen()
    header = "  " + "   ".join(chr(65 + i) for i in range(len(board[0])))
    print(header)
    print("+---" * len(board[0]) + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * len(board[0]) + "+")

def is_valid_input(choice, columns):
    """Check if the player's input is valid."""
    return choice.isalpha() and 0 <= ord(choice.upper()) - ord('A') < columns

def place_checker(board, column, marker):
    """Place the player's marker in the given column."""
    for row in reversed(board):
        if row[column] == " ":
            row[column] = marker
            return True
    return False

def check_for_win(board, marker):
    """Check for a win condition for the given marker."""
    # Check horizontal
    for row in board:
        for col in range(len(row) - 3):
            if all([row[col + i] == marker for i in range(4)]):
                return True
    
    # Check vertical
    for col in range(len(board[0])):
        for row in range(len(board) - 3):
            if all([board[row + i][col] == marker for i in range(4)]):
                return True

    # Check diagonal /
    for col in range(len(board[0]) - 3):
        for row in range(3, len(board)):
            if all([board[row - i][col + i] == marker for i in range(4)]):
                return True

    # Check diagonal \
    for col in range(len(board[0]) - 3):
        for row in range(len(board) - 3):
            if all([board[row + i][col + i] == marker for i in range(4)]):
                return True

    return False

def check_for_draw(board):
    """Check if the game is a draw."""
    return all(cell != " " for row in board for cell in row)

def main():
    board = create_board(ROWS, COLUMNS)
    player_turn = random.randint(0, PLAYERS - 1)
    print_board(board)

    while True:
        current_marker = PLAYER_MARKERS[player_turn]
        print(f"Player {current_marker}, please enter a column:")
        
        choice = input().strip()
        if not is_valid_input(choice, COLUMNS):
            print("Invalid input, please choose a valid column letter.")
            continue

        column = ord(choice.upper()) - ord('A')
        if not place_checker(board, column, current_marker):
            print("Column is full, choose another one.")
            continue

        print_board(board)

        if check_for_win(board, current_marker):
            print(f"Player {current_marker} won!")
            break

        if check_for_draw(board):
            print("It's a draw!")
            break

        # Switch to the next player
        player_turn = (player_turn + 1) % PLAYERS

if __name__ == "__main__":
    main()
