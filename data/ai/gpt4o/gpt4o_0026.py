import random
import os

# Constants for configuration
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

# Initializing the board
def create_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]

# Print the board
def print_board(board):
    os.system('clear')
    header = "  " + "   ".join(chr(ord('A') + i) for i in range(COLUMNS))
    print(header)
    print("+---" * COLUMNS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

# Check for a win
def check_win(board, player_checker):
    # Check horizontal, vertical, and diagonal wins
    for row in range(ROWS):
        for column in range(COLUMNS):
            # Check horizontal
            if column <= COLUMNS - 4:
                if all(board[row][column + i] == player_checker for i in range(4)):
                    return True
            # Check vertical
            if row <= ROWS - 4:
                if all(board[row + i][column] == player_checker for i in range(4)):
                    return True
            # Check diagonal (positive slope)
            if row <= ROWS - 4 and column <= COLUMNS - 4:
                if all(board[row + i][column + i] == player_checker for i in range(4)):
                    return True
            # Check diagonal (negative slope)
            if row >= 3 and column <= COLUMNS - 4:
                if all(board[row - i][column + i] == player_checker for i in range(4)):
                    return True
    return False

# Check for draw
def check_draw(board):
    return all(board[0][col] != " " for col in range(COLUMNS))

# Place a checker in the specified column
def place_checker(board, column, player_checker):
    for row in reversed(range(ROWS)):
        if board[row][column] == " ":
            board[row][column] = player_checker
            return True
    return False

# Validate user input
def validate_input(input_str):
    if len(input_str) == 1 and input_str.isalpha():
        column = ord(input_str.upper()) - ord('A')
        if 0 <= column < COLUMNS:
            return column
    return -1

def main():
    board = create_board(ROWS, COLUMNS)
    # Randomly select the first player
    current_player_index = random.randint(0, MAX_PLAYERS - 1)
    
    # Main game loop
    while True:
        print_board(board)
        current_player_checker = CHECKERS[current_player_index]
        print(f"Player {current_player_checker}, please enter a column:")
        
        valid_move = False
        while not valid_move:
            user_input = input()
            column = validate_input(user_input)
            if column != -1:
                if place_checker(board, column, current_player_checker):
                    valid_move = True
                else:
                    print("The column is full, try another column.")
            else:
                print("Invalid input, please enter a valid column letter (A-G).")
        
        # Check for win
        if check_win(board, current_player_checker):
            print_board(board)
            print(f"Player {current_player_checker} won!")
            break
        
        # Check for draw
        if check_draw(board):
            print_board(board)
            print("The game is a draw!")
            break
        
        # Alternate to the next player
        current_player_index = (current_player_index + 1) % MAX_PLAYERS

if __name__ == "__main__":
    main()
