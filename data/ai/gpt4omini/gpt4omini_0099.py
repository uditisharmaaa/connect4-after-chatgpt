import os
import random

# Constants for board dimensions and player checkers
ROWS = 6
COLS = 7
PLAYERS = ["X", "O", "V", "H", "M"]  # Support up to 5 players

def create_board():
    """Create an empty game board."""
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the game board."""
    os.system('clear')  # Clear the terminal screen
    print("  " + "   ".join(chr(65 + c) for c in range(COLS)))  # Column labels A-G
    print("+---+" + "---+" * (COLS - 1))
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---+" + "---+" * (COLS - 1))

def is_valid_move(board, column):
    """Check if the move is valid (i.e., column is within range and not full)."""
    return 0 <= column < COLS and board[0][column] == " "

def place_checker(board, column, checker):
    """Place the checker in the specified column."""
    for row in reversed(board):
        if row[column] == " ":
            row[column] = checker
            return True
    return False

def check_winner(board, checker):
    """Check for a win condition for the specified checker."""
    # Check horizontal, vertical, and diagonal wins
    for r in range(ROWS):
        for c in range(COLS):
            if c + 3 < COLS and all(board[r][c + i] == checker for i in range(4)):
                return True
            if r + 3 < ROWS and all(board[r + i][c] == checker for i in range(4)):
                return True
            if r + 3 < ROWS and c + 3 < COLS and all(board[r + i][c + i] == checker for i in range(4)):
                return True
            if r - 3 >= 0 and c + 3 < COLS and all(board[r - i][c + i] == checker for i in range(4)):
                return True
    return False

def is_draw(board):
    """Check if the game is a draw (board is full)."""
    return all(board[0][c] != " " for c in range(COLS))

def main():
    board = create_board()
    current_player = random.randint(0, min(len(PLAYERS)-1, 1))  # Randomly select first player
    game_over = False

    while not game_over:
        print_board(board)
        checker = PLAYERS[current_player]
        column = input(f"Player {checker}, please enter a column (A-{chr(65 + COLS - 1)}): ").upper()
        
        if len(column) != 1 or not column.isalpha() or not (ord(column) - 65 in range(COLS)):
            print("Invalid input. Please enter a valid column.")
            continue  # Ask for input again

        column = ord(column) - 65  # Convert to column index
        
        if is_valid_move(board, column):
            place_checker(board, column, checker)
            if check_winner(board, checker):
                print_board(board)
                print(f"Player {checker} won!")
                game_over = True
            elif is_draw(board):
                print_board(board)
                print("The game is a draw!")
                game_over = True
            else:
                current_player = (current_player + 1) % len(PLAYERS)  # Switch to the next player
        else:
            print("Column is full. Please select another column.")

if __name__ == "__main__":
    main()
