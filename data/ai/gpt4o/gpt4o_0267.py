import random
import os

# Constants
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
CHECKERS = ["X", "O", "V", "H", "M"]
EMPTY_CELL = " "
WINNING_COUNT = 4

def init_board(rows, columns):
    """Initialize the game board with empty cells."""
    return [[EMPTY_CELL for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    """Display the board."""
    os.system('clear')  # For UNIX systems
    print("  " + "   ".join(chr(ord('A') + i) for i in range(COLUMNS)))
    print("+---" * COLUMNS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

def is_valid_input(input_str, columns):
    """Check if the input is valid."""
    return len(input_str) == 1 and input_str.isalpha() and ord(input_str.upper()) - ord('A') < columns

def place_checker(board, column, checker):
    """Place the checker's piece in the specified column."""
    col_idx = ord(column.upper()) - ord('A')
    for row in reversed(board):
        if row[col_idx] == EMPTY_CELL:
            row[col_idx] = checker
            return True
    return False

def check_win(board, rows, columns, winning_count):
    """Check all conditions for a win."""
    def check_line(line):
        count = 0
        last_checker = None
        for cell in line:
            if cell == last_checker and cell != EMPTY_CELL:
                count += 1
            else:
                count = 1
                last_checker = cell
            if count >= winning_count:
                return True
        return False

    # Check horizontal
    for row in board:
        if check_line(row):
            return True
    
    # Check vertical
    for col in range(columns):
        if check_line([board[row][col] for row in range(rows)]):
            return True

    # Check diagonal (top-left to bottom-right)
    for r in range(rows - winning_count + 1):
        for c in range(columns - winning_count + 1):
            if check_line([board[r + i][c + i] for i in range(winning_count)]):
                return True

    # Check diagonal (bottom-left to top-right)
    for r in range(winning_count - 1, rows):
        for c in range(columns - winning_count + 1):
            if check_line([board[r - i][c + i] for i in range(winning_count)]):
                return True

    return False

def check_draw(board):
    """Check if the board is completely filled."""
    return all(cell != EMPTY_CELL for row in board for cell in row)

def play_game(rows=ROWS, columns=COLUMNS, player_count=2):
    """Run the Connect 4 game."""
    board = init_board(rows, columns)
    current_player = random.randint(0, player_count - 1)
    print_board(board)

    while True:
        current_checker = CHECKERS[current_player]
        print(f"Player {current_checker}, please enter a column:")
        while True:
            user_input = input().strip()
            if is_valid_input(user_input, columns):
                if place_checker(board, user_input, current_checker):
                    break
                else:
                    print("Column is full! Choose another column or lose your turn.")
                    break
            else:
                print("Invalid input! Please enter a valid column letter.")
        
        print_board(board)

        if check_win(board, rows, columns, WINNING_COUNT):
            print(f"Player {current_checker} won!")
            break
        
        if check_draw(board):
            print("The game is a draw!")
            break

        current_player = (current_player + 1) % player_count

# Game starts
if __name__ == "__main__":
    play_game()
