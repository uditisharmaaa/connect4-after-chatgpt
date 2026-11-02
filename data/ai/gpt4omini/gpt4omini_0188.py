import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O']  # You can change this list to support more players

# Create the game board
def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

# Print the game board
def print_board(board):
    os.system('clear')  # Clear the screen
    print('  ' + '   '.join(chr(65 + i) for i in range(COLS)))  # Column labels (A, B, C, ...)
    print('+' + '---+' * COLS)  # Top border
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')  # Board rows
        print('+' + '---+' * COLS)  # Row separators

# Check if a move is valid
def is_valid_move(board, col):
    return board[0][col] == ' '

# Place the checker in the specified column
def place_checker(board, col, checker):
    for row in reversed(range(ROWS)):
        if board[row][col] == ' ':
            board[row][col] = checker
            return True
    return False

# Check for a win
def check_win(board, checker):
    # Check horizontal, vertical, and diagonal wins
    # Horizontal check
    for r in range(ROWS):
        for c in range(COLS - 3):
            if all(board[r][c + i] == checker for i in range(4)):
                return True

    # Vertical check
    for c in range(COLS):
        for r in range(ROWS - 3):
            if all(board[r + i][c] == checker for i in range(4)):
                return True

    # Diagonal check (positive slope)
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if all(board[r + i][c + i] == checker for i in range(4)):
                return True

    # Diagonal check (negative slope)
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if all(board[r - i][c + i] == checker for i in range(4)):
                return True

    return False

# Check for a draw
def check_draw(board):
    return all(board[0][c] != ' ' for c in range(COLS))

# Main game loop
def play_game():
    board = create_board()
    current_player_index = random.randint(0, len(PLAYERS) - 1)
    total_turns = 0
    max_turns = ROWS * COLS

    while total_turns < max_turns:
        current_player = PLAYERS[current_player_index]
        print_board(board)
        print(f"Player {current_player}, please enter a column (A-G):")

        while True:
            try:
                col_input = input().upper()
                if len(col_input) != 1 or col_input < 'A' or col_input > chr(64 + COLS):
                    raise ValueError("Invalid column. Choose between A and G.")
                col = ord(col_input) - 65  # Convert character to column index
                if is_valid_move(board, col):
                    place_checker(board, col, current_player)
                    break
                else:
                    print("Column is full! Choose another column.")
            except (ValueError, IndexError):
                print("Invalid input! Please enter a valid column (A-G):")

        # Check for win or draw
        if check_win(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            return
        if check_draw(board):
            print_board(board)
            print("The game is a draw!")
            return

        # Move to the next player
        current_player_index = (current_player_index + 1) % len(PLAYERS)
        total_turns += 1

if __name__ == "__main__":
    play_game()
