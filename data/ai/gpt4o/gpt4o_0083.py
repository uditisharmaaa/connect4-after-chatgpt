import os
import random

# Global constants
ROWS = 6
COLUMNS = 7
PLAYER_COUNT = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']  # Handles up to 5 players

def clear_screen():
    os.system('clear')

def create_board():
    """Create a 2D list for the board."""
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    """Print the board with column labels."""
    clear_screen()
    # Prepare column labels
    column_labels = "  ".join(chr(65 + i) for i in range(COLUMNS))
    print(f"  {column_labels}")
    print("+---" * COLUMNS + "+")

    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

def is_valid_input(input_str):
    """Check if the input is a valid column character."""
    return len(input_str) == 1 and input_str.isalpha() and ord(input_str.upper()) - 65 < COLUMNS

def place_checker(board, column, checker):
    """Place the checker in the lowest available space in the column."""
    column_index = ord(column.upper()) - 65

    for i in range(ROWS-1, -1, -1):
        if board[i][column_index] == " ":
            board[i][column_index] = checker
            return True
    
    return False  # Column is full

def check_for_win(board, checker):
    """Check for 4 in a row horizontally, vertically, or diagonally."""
    # Horizontal Check
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col+i] == checker for i in range(4)):
                return True

    # Vertical Check
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row+i][col] == checker for i in range(4)):
                return True

    # Diagonal Check (/)
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row-i][col+i] == checker for i in range(4)):
                return True

    # Diagonal Check (\)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row+i][col+i] == checker for i in range(4)):
                return True

    return False

def check_for_draw(board):
    """Check if the board is completely filled without any winner."""
    return all(board[0][col] != " " for col in range(COLUMNS))

def main():
    board = create_board()
    current_player_index = random.randint(0, PLAYER_COUNT - 1)
    current_checker = CHECKERS[current_player_index]
    
    print_board(board)
    
    while True:
        player_entry = input(f"Player {current_checker}, please enter a column: ")

        if not is_valid_input(player_entry):
            print("Invalid input, please enter a valid column letter.")
            continue

        if not place_checker(board, player_entry, current_checker):
            print("Column full, you lost your turn.")
        else:
            print_board(board)
            if check_for_win(board, current_checker):
                print(f"Player {current_checker} won!")
                break
            if check_for_draw(board):
                print("Game is a draw!")
                break
            
            # Alternate player
            current_player_index = (current_player_index + 1) % PLAYER_COUNT
            current_checker = CHECKERS[current_player_index]

if __name__ == "__main__":
    main()
