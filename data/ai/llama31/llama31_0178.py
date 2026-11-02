import os
import random
import string

# Constants
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    """Create a 2D board with all elements initialized to whitespaces."""
    return [[' ' for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]

def print_board(board):
    """Print the current state of the board."""
    os.system('clear')
    print('  ' + '   '.join(string.ascii_uppercase[:NUM_COLS]))
    for row in board:
        print('+---' * NUM_COLS + '+')
        print('| ' + ' | '.join(row) + ' |')
    print('+---' * NUM_COLS + '+')

def validate_input(player, board):
    """Validate the user input and ask for another input if it's invalid."""
    while True:
        col = input(f"Player {player}, please enter a column: ").strip().upper()
        if col not in string.ascii_uppercase[:NUM_COLS]:
            print("Invalid input. Please enter a letter between A and G.")
        elif board[NUM_ROWS-1][string.ascii_uppercase.index(col)]!= ' ':
            print("Column is already full. Please choose another column.")
        else:
            return string.ascii_uppercase.index(col)

def place_checker(board, player, col):
    """Place the checker at the correct location on the board."""
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = player
            break

def check_win(board, player):
    """Check if the current player has won the game."""
    # Check horizontal wins
    for row in board:
        for i in range(NUM_COLS - 3):
            if row[i] == player and row[i+1] == player and row[i+2] == player and row[i+3] == player:
                return True
    # Check vertical wins
    for col in range(NUM_COLS):
        for i in range(NUM_ROWS - 3):
            if board[i][col] == player and board[i+1][col] == player and board[i+2][col] == player and board[i+3][col] == player:
                return True
    # Check diagonal wins (top-left to bottom-right)
    for row in range(NUM_ROWS - 3):
        for col in range(NUM_COLS - 3):
            if board[row][col] == player and board[row+1][col+1] == player and board[row+2][col+2] == player and board[row+3][col+3] == player:
                return True
    # Check diagonal wins (bottom-left to top-right)
    for row in range(3, NUM_ROWS):
        for col in range(NUM_COLS - 3):
            if board[row][col] == player and board[row-1][col+1] == player and board[row-2][col+2] == player and board[row-3][col+3] == player:
                return True
    return False

def check_draw(board):
    """Check if the game is a draw."""
    return all(cell!= ' ' for row in board for cell in row)

def main():
    board = create_board()
    players = CHECKERS[:NUM_PLAYERS]
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    while True:
        print_board(board)
        current_player = players[current_player_index]
        col = validate_input(current_player, board)
        place_checker(board, current_player, col)
        if check_win(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break
        elif check_draw(board):
            print_board(board)
            print("It's a draw!")
            break
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
