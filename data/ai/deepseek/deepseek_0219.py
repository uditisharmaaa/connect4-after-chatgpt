import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M'][:PLAYERS]

def clear_screen():
    """Clear the terminal screen."""
    os.system('clear' if os.name == 'posix' else 'cls')

def create_board():
    """Create an empty game board with the specified dimensions."""
    return [[ ' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the game board with column labels."""
    # Print column headers
    header = '  '
    for col in range(COLS):
        header += f"{chr(65 + col)}   "
    print(header)

    # Print each row with borders
    border = "+" + ("---+" * COLS)
    print(border)
    for row in board:
        row_str = "|"
        for cell in row:
            row_str += f" {cell} |"
        print(row_str)
        print(border)

def is_valid_column(column):
    """Check if the column input is valid."""
    if len(column) != 1:
        return False
    col = ord(column.upper()) - ord('A')
    return 0 <= col < COLS

def drop_checker(board, col, checker):
    """Place the checker in the lowest empty row of the specified column."""
    for row in range(ROWS-1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = checker
            return True
    return False

def check_win(board, checker):
    """Check if the current player has won."""
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col+i] == checker for i in range(4)):
                return True

    # Check vertical
    for row in range(ROWS - 3):
        for col in range(COLS):
            if all(board[row+i][col] == checker for i in range(4)):
                return True

    # Check diagonal (top-left to bottom-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row+i][col+i] == checker for i in range(4)):
                return True

    # Check diagonal (bottom-left to top-right)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row-i][col+i] == checker for i in range(4)):
                return True

    return False

def is_board_full(board):
    """Check if all cells in the board are occupied."""
    return all(cell != ' ' for row in board for cell in row)

def main():
    """Main function to run the Connect 4 game."""
    board = create_board()
    current_player = random.randint(0, PLAYERS - 1)
    game_over = False

    while not game_over:
        clear_screen()
        print_board(board)
        checker = CHECKERS[current_player]
        print(f"Player {checker}, please enter a column: ", end='')
        
        while True:
            column = input().upper()
            if is_valid_column(column):
                col = ord(column) - ord('A')
                if drop_checker(board, col, checker):
                    break
                else:
                    print("Column is full. Try another column: ", end='')
            else:
                print("Invalid input. Please enter a valid column (A-G): ", end='')

        if check_win(board, checker):
            clear_screen()
            print_board(board)
            print(f"Player {checker} won!")
            game_over = True
        elif is_board_full(board):
            clear_screen()
            print_board(board)
            print("It's a draw!")
            game_over = True
        else:
            current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
