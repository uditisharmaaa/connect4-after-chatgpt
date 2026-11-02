import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYER_CHECKERS = ['X', 'O']
MAX_PLAYERS = 5
WIN_COUNT = 4

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')

def create_board():
    """Creates an empty board with dimensions ROWS x COLUMNS."""
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    """Prints the current state of the board."""
    clear_screen()
    print('  ' + '   '.join([chr(ord('A') + i) for i in range(COLUMNS)]))
    print('+---' * COLUMNS + '+')
    for row in board:
        print('| ' + ' | '.join(row) + ' |')
        print('+---' * COLUMNS + '+')

def is_valid_input(column_input):
    """Checks if the column input by the player is valid."""
    if len(column_input) != 1 or not column_input.isalpha():
        return False
    column_index = ord(column_input.upper()) - ord('A')
    return 0 <= column_index < COLUMNS

def place_checker(board, column_input, checker):
    """Places the checker in the chosen column if possible."""
    column_index = ord(column_input.upper()) - ord('A')
    for row in reversed(board):
        if row[column_index] == ' ':
            row[column_index] = checker
            return True
    return False

def check_winner(board, checker):
    """Checks if there is a winning configuration on the board."""
    # Check horizontal
    for row in board:
        for col in range(COLUMNS - WIN_COUNT + 1):
            if all(row[col + i] == checker for i in range(WIN_COUNT)):
                return True
    
    # Check vertical
    for col in range(COLUMNS):
        for row in range(ROWS - WIN_COUNT + 1):
            if all(board[row + i][col] == checker for i in range(WIN_COUNT)):
                return True
    
    # Check diagonal /
    for row in range(ROWS - WIN_COUNT + 1):
        for col in range(COLUMNS - WIN_COUNT + 1):
            if all(board[row + i][col + i] == checker for i in range(WIN_COUNT)):
                return True
    
    # Check diagonal \
    for row in range(WIN_COUNT - 1, ROWS):
        for col in range(COLUMNS - WIN_COUNT + 1):
            if all(board[row - i][col + i] == checker for i in range(WIN_COUNT)):
                return True
    
    return False

def check_draw(board):
    """Checks if the board is in a draw state."""
    return all(cell != ' ' for row in board for cell in row)

def main():
    board = create_board()
    num_players = len(PLAYER_CHECKERS)
    current_player = random.randint(0, num_players - 1)
    print_board(board)
    
    while True:
        checker = PLAYER_CHECKERS[current_player]
        print(f"Player {checker}, please enter a column:")
        column_input = input().strip()
        
        if not is_valid_input(column_input):
            print("Invalid input. Please enter a valid column letter.")
            continue
        
        if not place_checker(board, column_input, checker):
            print("Column is full. You lose your turn.")
        else:
            print_board(board)
            
            if check_winner(board, checker):
                print(f"Player {checker} won!")
                break
            
            if check_draw(board):
                print("It's a draw!")
                break
        
        current_player = (current_player + 1) % num_players

if __name__ == "__main__":
    main()
