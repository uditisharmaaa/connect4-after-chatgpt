import os
import random

# Constants for configuration, adjust as needed
ROWS = 6
COLUMNS = 7
PLAYER_COUNT = 2
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"][:PLAYER_COUNT]

def create_board(rows, columns):
    """Initializes the game board."""
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    """Prints the current state of the board."""
    os.system('clear')
    header = "   " + "   ".join(chr(65 + i) for i in range(COLUMNS))
    print(header)
    for row in board:
        print("+---" * COLUMNS + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * COLUMNS + "+")

def get_valid_column_input():
    """Gets a valid column input from the player."""
    while True:
        column_input = input("Please enter a column: ").strip().upper()
        if len(column_input) == 1 and 'A' <= column_input < chr(65 + COLUMNS):
            return ord(column_input) - 65
        else:
            print("Invalid input. Please enter a valid column letter.")

def place_checker(board, column, symbol):
    """Places the checker in the chosen column if possible."""
    for row in reversed(board):
        if row[column] == " ":
            row[column] = symbol
            return True
    return False

def check_for_win(board, symbol):
    """Checks for a winner on the board."""
    # Horizontal check
    for row in board:
        for col in range(COLUMNS - 3):
            if row[col:col+4] == [symbol] * 4:
                return True
                
    # Vertical check
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row+i][col] == symbol for i in range(4)):
                return True
                
    # Diagonal checks
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row+i][col+i] == symbol for i in range(4)):
                return True
        for col in range(3, COLUMNS):
            if all(board[row+i][col-i] == symbol for i in range(4)):
                return True
                
    return False

def check_for_draw(board):
    """Checks if the game is a draw."""
    return all(cell != " " for row in board for cell in row)

def play_connect_4():
    """Main function to play Connect 4."""
    board = create_board(ROWS, COLUMNS)
    current_player = random.choice(PLAYER_SYMBOLS)
    print_board(board)
    
    while True:
        print(f"Player {current_player}'s turn.")
        column = get_valid_column_input()
        
        if place_checker(board, column, current_player):
            print_board(board)
            
            if check_for_win(board, current_player):
                print(f"Player {current_player} won!")
                break
                
            if check_for_draw(board):
                print("The game is a draw!")
                break
                
            current_player = PLAYER_SYMBOLS[(PLAYER_SYMBOLS.index(current_player) + 1) % PLAYER_COUNT]
        else:
            print(f"Column {chr(65 + column)} is full, choose another column.")

if __name__ == "__main__":
    play_connect_4()
