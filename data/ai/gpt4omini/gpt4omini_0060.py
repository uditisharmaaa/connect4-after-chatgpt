import os
import random

# Constants for the game
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    """Creates an empty game board."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Prints the current state of the board."""
    os.system('clear' if os.name == 'posix' else 'cls')
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))  # Column labels A, B, C, ...
    print("+---" + "---+" * (COLS - 1) + "---+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" + "---+" * (COLS - 1) + "---+")

def is_valid_input(column, board):
    """Validates user input for the column."""
    if column < 0 or column >= COLS:
        return False
    if board[0][column] != ' ':  # Check if the top of the column is occupied
        return False
    return True

def place_checker(board, column, checker):
    """Places a checker in the specified column."""
    for row in reversed(board):
        if row[column] == ' ':
            row[column] = checker
            return True
    return False

def check_win(board, checker):
    """Checks if the specified checker has won."""
    # Check horizontal
    for row in board:
        for col in range(COLS - 3):
            if all(row[col + i] == checker for i in range(4)):
                return True

    # Check vertical
    for col in range(COLS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == checker for i in range(4)):
                return True

    # Check diagonals
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True
        for col in range(3, COLS):
            if all(board[row + i][col - i] == checker for i in range(4)):
                return True

    return False

def check_draw(board):
    """Checks if the game is a draw."""
    return all(board[0][col] != ' ' for col in range(COLS))

def main():
    board = create_board()
    current_player_index = random.randint(0, len(PLAYERS) - 1)
    
    print_board(board)
    
    while True:
        current_checker = PLAYERS[current_player_index]
        print(f"Player {current_checker}, please enter a column (A-G): ")
        
        while True:
            user_input = input().strip().upper()
            if user_input in (chr(65 + i) for i in range(COLS)):  # A-G
                column = ord(user_input) - 65
                if is_valid_input(column, board):
                    place_checker(board, column, current_checker)
                    break
                else:
                    print("Column is full or invalid! Please choose another column.")
            else:
                print("Invalid input! Please enter a valid column (A-G).")
        
        print_board(board)
        
        if check_win(board, current_checker):
            print(f"Player {current_checker} won!")
            break
        
        if check_draw(board):
            print("The game is a draw!")
            break
        
        current_player_index = (current_player_index + 1) % len(PLAYERS)

if __name__ == "__main__":
    main()
