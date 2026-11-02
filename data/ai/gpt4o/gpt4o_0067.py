import os
import random

# Constants for board dimensions and number of players
ROWS = 6
COLS = 7
PLAYERS = 2
PLAYER_MARKERS = ['X', 'O', 'V', 'H', 'M']  # Potential markers for up to 5 players

def create_board(rows, cols):
    """Initialize the board with empty spaces."""
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Print the board with column labels."""
    os.system('clear')  # Clear the terminal screen
    column_labels = '   '.join(chr(i) for i in range(65, 65 + COLS))
    print(f"  {column_labels}")
    print("+" + "---+" * COLS)

    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)

def is_valid_input(input, cols):
    """Check if the input is a valid column letter."""
    return input.isalpha() and len(input) == 1 and 'A' <= input <= chr(64 + cols)

def place_checker(board, col, marker):
    """Place a marker in the lowest available row in the specified column."""
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = marker
            return True
    return False

def check_winner(board, marker):
    """Check for winning conditions."""
    # Horizontal check
    for row in board:
        for col in range(COLS - 3):
            if all(row[col + i] == marker for i in range(4)):
                return True

    # Vertical check
    for col in range(COLS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == marker for i in range(4)):
                return True

    # Diagonal check (/ direction)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i][col + i] == marker for i in range(4)):
                return True

    # Diagonal check (\ direction)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == marker for i in range(4)):
                return True
    
    return False

def is_draw(board):
    """Check if the board is full, resulting in a draw."""
    return all(all(col != ' ' for col in row) for row in board)

def main():
    board = create_board(ROWS, COLS)
    current_player = random.randint(0, PLAYERS - 1)
    player_markers = PLAYER_MARKERS[:PLAYERS]

    print_board(board)

    while True:
        current_marker = player_markers[current_player]
        user_input = input(f"Player {current_marker}, please enter a column: ").strip().upper()

        if not is_valid_input(user_input, COLS):
            print("Invalid input. Please enter a valid column letter.")
            continue

        col_index = ord(user_input) - 65

        if place_checker(board, col_index, current_marker):
            print_board(board)
            if check_winner(board, current_marker):
                print(f"Player {current_marker} won!")
                break
            if is_draw(board):
                print("The game is a draw!")
                break
            current_player = (current_player + 1) % PLAYERS
        else:
            print("Column is full. You lose your turn.")

if __name__ == "__main__":
    main()
