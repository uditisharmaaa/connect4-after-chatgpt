import os
import random

# Constants for the game configuration
ROWS = 6
COLUMNS = 7
PLAYERS = 2
PLAYER_MARKERS = ['X', 'O', 'V', 'H', 'M']  # Max 5 players supported

def initialize_board(rows, cols):
    """Initializes the game board with empty spaces."""
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Prints the game board."""
    os.system('clear')  # Clear the console screen
    print("\n  " + "   ".join(chr(65 + col) for col in range(len(board[0]))))
    print("+" + "---+" * len(board[0]))
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * len(board[0]))

def valid_input(input_str, cols):
    """Checks if the input from the player is valid."""
    if len(input_str) == 1 and 'A' <= input_str <= 'G' and ord(input_str) - 65 < cols:
        return True
    return False

def drop_checker(board, col, marker):
    """Drops the checker into the board for a given column."""
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = marker
            return True
    return False  # Column is full

def check_winner(board, marker):
    """Checks if there's a winner on the board."""
    # Horizontal check
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col + i] == marker for i in range(4)):
                return True

    # Vertical check
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == marker for i in range(4)):
                return True

    # Diagonal checks (top-left to bottom-right)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == marker for i in range(4)):
                return True

    # Diagonal checks (bottom-left to top-right)
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row - i][col + i] == marker for i in range(4)):
                return True

    return False

def check_draw(board):
    """Checks if the game is a draw."""
    return all(board[0][col] != ' ' for col in range(COLUMNS))

def main():
    board = initialize_board(ROWS, COLUMNS)
    current_player = random.randint(0, PLAYERS - 1)
    player_markers = PLAYER_MARKERS[:PLAYERS]

    print_board(board)

    while True:
        print(f"Player {player_markers[current_player]}, please enter a column:")
        player_input = input().strip().upper()

        if not valid_input(player_input, COLUMNS):
            print("Invalid input. Please choose a valid column letter (A-G).")
            continue

        col_index = ord(player_input) - 65

        if not drop_checker(board, col_index, player_markers[current_player]):
            print("Column is full. Try a different column.")
            continue

        print_board(board)

        if check_winner(board, player_markers[current_player]):
            print(f"Player {player_markers[current_player]} won!")
            break
        
        if check_draw(board):
            print("The game is a draw!")
            break

        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
