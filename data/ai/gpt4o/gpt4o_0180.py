import os
import random

# Constants for board dimensions and number of players
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    """Creates a board with specified dimensions and initializes it with whitespaces."""
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    """Clears the screen and prints the current state of the board."""
    os.system('clear')
    header = "  " + "   ".join(chr(65+i) for i in range(COLUMNS))
    print(header)
    print("+" + "---+" * COLUMNS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLUMNS)

def switch_player(current_player):
    """Switches to the next player."""
    return (current_player + 1) % PLAYERS

def is_valid_input(column, board):
    """Checks if the input column is valid and not completely filled."""
    if column < 0 or column >= COLUMNS or board[0][column] != ' ':
        return False
    return True

def drop_checker(board, column, checker):
    """Places the checker in the lowest available position in the specified column."""
    for row in range(ROWS-1, -1, -1):
        if board[row][column] == ' ':
            board[row][column] = checker
            break

def check_win(board, checker):
    """Checks for any winning condition on the board for the given player."""
    # Horizontal, Vertical, Diagonal Checks
    for row in range(ROWS):
        for col in range(COLUMNS-3):
            if all(board[row][c] == checker for c in range(col, col+4)):
                return True
    for col in range(COLUMNS):
        for row in range(ROWS-3):
            if all(board[r][col] == checker for r in range(row, row+4)):
                return True
    for row in range(ROWS-3):
        for col in range(COLUMNS-3):
            if all(board[row+i][col+i] == checker for i in range(4)):
                return True
            if all(board[row+3-i][col+i] == checker for i in range(4)):
                return True
    return False

def check_draw(board):
    """Checks if the board is completely filled without any winner."""
    return all(board[0][col] != ' ' for col in range(COLUMNS))

def play_connect4():
    """Main function to run the Connect 4 game."""
    board = create_board()
    current_player = random.randint(0, PLAYERS-1)
    print_board(board)
    
    while True:
        checker = CHECKERS[current_player]
        while True:
            try:
                choice = input(f"Player {checker}, please enter a column: ").strip().upper()
                column = ord(choice) - 65
                if is_valid_input(column, board):
                    break
                else:
                    print("Invalid input or column full. Try again.")
            except (IndexError, ValueError):
                print("Invalid input. Try again.")

        drop_checker(board, column, checker)
        print_board(board)
        
        if check_win(board, checker):
            print(f"Player {checker} won!")
            break
        elif check_draw(board):
            print("It's a draw!")
            break
        else:
            current_player = switch_player(current_player)

if __name__ == "__main__":
    play_connect4()
