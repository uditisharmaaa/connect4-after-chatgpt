import random
import os

# Constants for board dimensions and number of players
ROWS = 6
COLS = 7
PLAYERS = 2

# Player checkers
CHECKERS = ['X', 'O', 'V', 'H', 'M']

# Initialize board
def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

# Print the board with labels
def print_board(board):
    os.system('clear')
    print('  ' + '   '.join(chr(c) for c in range(ord('A'), ord('A') + COLS)))
    print('+---' * COLS + '+')
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+---' * COLS + '+')

# Determine if the input is valid
def is_valid_input(choice, board):
    if len(choice) != 1:
        return False
    col = ord(choice.upper()) - ord('A')
    if 0 <= col < COLS:
        return board[0][col] == ' '
    return False

# Place the checker in the chosen column
def place_checker(choice, board, checker):
    col = ord(choice.upper()) - ord('A')
    for row in reversed(range(ROWS)):
        if board[row][col] == ' ':
            board[row][col] = checker
            return row, col

# Check if there is a winning sequence
def is_winning_move(board, checker):
    # Horizontal check
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True

    # Vertical check
    for col in range(COLS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == checker for i in range(4)):
                return True

    # Diagonal / check
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True

    # Diagonal \ check
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True

    return False

# Check if the board is full
def is_draw(board):
    return all(board[0][col] != ' ' for col in range(COLS))

# Main game loop
def play_game():
    # Create the board
    board = create_board()

    # Randomly select the first player
    current_player = random.randint(0, PLAYERS - 1)

    # Main game loop
    while True:
        print_board(board)
        print(f"Player {CHECKERS[current_player]}'s turn:")
        
        # Get valid column choice
        choice = input("Player, please enter a column: ").strip().upper()
        while not is_valid_input(choice, board):
            choice = input("Invalid input. Please enter a column: ").strip().upper()
        
        # Place checker
        row, col = place_checker(choice, board, CHECKERS[current_player])

        # Check for win
        if is_winning_move(board, CHECKERS[current_player]):
            print_board(board)
            print(f"Player {CHECKERS[current_player]} won!")
            break

        # Check for draw
        if is_draw(board):
            print_board(board)
            print("The game is a draw!")
            break

        # Switch players
        current_player = (current_player + 1) % PLAYERS

# Start the game
if __name__ == "__main__":
    play_game()
