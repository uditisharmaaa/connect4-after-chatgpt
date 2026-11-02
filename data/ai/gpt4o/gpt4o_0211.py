import os
import random

# Constants for the game
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']  # Checkers for more than 2 players
MAX_COLUMNS = 26

def create_board(rows, columns):
    """Initialize the game board with empty spaces."""
    return [[' ' for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    """Print the current state of the board."""
    os.system('clear')  # Clear the screen

    # Print column labels
    print('  ' + '   '.join(chr(c) for c in range(65, 65 + len(board[0]))))
    print('+---' * len(board[0]) + '+')

    # Print rows of the board
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+---' * len(board[0]) + '+')
        
def valid_input(input_str, columns):
    """Check if the player's input is valid."""
    if len(input_str) == 1 and ord(input_str) >= 65 and ord(input_str) < 65 + columns:
        return True
    return False

def drop_checker(board, column, checker):
    """Place the checker in the lowest available position in the column."""
    for row in reversed(board):
        if row[column] == ' ':
            row[column] = checker
            return True
    return False

def check_winner(board, checker):
    """Check for a winning condition."""
    rows, columns = len(board), len(board[0])
    
    # Horizontal check
    for row in range(rows):
        for col in range(columns - 3):
            if all(board[row][col+i] == checker for i in range(4)):
                return True

    # Vertical check
    for col in range(columns):
        for row in range(rows - 3):
            if all(board[row+i][col] == checker for i in range(4)):
                return True

    # Diagonal checks
    for row in range(rows - 3):
        for col in range(columns - 3):
            if all(board[row+i][col+i] == checker for i in range(4)):
                return True
    for row in range(3, rows):
        for col in range(columns - 3):
            if all(board[row-i][col+i] == checker for i in range(4)):
                return True

    return False

def is_draw(board):
    """Check if the game is a draw (board is full)."""
    return all(cell != ' ' for row in board for cell in row)

def main():
    board = create_board(ROWS, COLUMNS)
    current_player_idx = random.randint(0, PLAYERS - 1)
    game_over = False

    print_board(board)

    while not game_over:
        current_checker = CHECKERS[current_player_idx]
        player_input = input(f"Player {current_checker}, please enter a column: ").strip().upper()

        if valid_input(player_input, COLUMNS):
            column_idx = ord(player_input) - 65
            if drop_checker(board, column_idx, current_checker):
                print_board(board)
                
                if check_winner(board, current_checker):
                    print(f"Player {current_checker} won!")
                    game_over = True
                elif is_draw(board):
                    print("The game is a draw!")
                    game_over = True
                else:
                    current_player_idx = (current_player_idx + 1) % PLAYERS
            else:
                print("Column is full! Turn is invalid.")
        else:
            print("Invalid input. Please enter a valid column letter.")

if __name__ == "__main__":
    main()
