import os
import random

# Constants for default settings
ROWS = 6
COLUMNS = 7
MAX_COLUMNS = 26
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]  # Possible checkers for up to 5 players

def clear_screen():
    os.system('clear')

def create_board(rows, columns):
    """Initialize the game board with empty spaces."""
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    """Print the board on the screen."""
    clear_screen()
    columns = len(board[0])
    print("  " + "   ".join(chr(65 + i) for i in range(columns)))
    print("+---" * columns + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * columns + "+")

def is_valid_column(input_char, columns):
    """Validate if the input character corresponds to a valid column."""
    return input_char.isalpha() and 0 <= ord(input_char.upper()) - 65 < columns

def place_checker(board, column, checker):
    """Place the checker in the first available row in the specified column."""
    for row in reversed(board):
        if row[column] == " ":
            row[column] = checker
            return True
    return False

def check_winner(board, required_checkers):
    """Check for a winner (4 checkers in a row) after each turn."""
    rows, columns = len(board), len(board[0])
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]  # Right, Down, Diagonal Right Down, Diagonal Left Down

    for row in range(rows):
        for col in range(columns):
            if board[row][col] != " ":
                for direction in directions:
                    consecutive_count = 0
                    for step in range(required_checkers):
                        r, c = row + step * direction[0], col + step * direction[1]
                        if r < rows and c < columns and board[r][c] == board[row][col]:
                            consecutive_count += 1
                        else:
                            break
                    if consecutive_count == required_checkers:
                        return True
    return False

def check_draw(board):
    """Check if the board is fully occupied, indicating a draw."""
    return all(cell != " " for row in board for cell in row)

def play_game(rows, columns, num_players):
    """Manage the game flow."""
    board = create_board(rows, columns)
    print_board(board)
    
    checkers = CHECKERS[:num_players]
    current_player = random.randint(0, num_players - 1)

    while True:
        print(f"Player {checkers[current_player]}, please enter a column:")
        while True:
            input_column = input().upper()
            if is_valid_column(input_column, columns):
                column_index = ord(input_column) - 65
                if place_checker(board, column_index, checkers[current_player]):
                    break
                else:
                    print("Column is full. Please choose another column.")
            else:
                print("Invalid column. Please enter a valid letter.")

        print_board(board)
        
        if check_winner(board, 4):
            print(f"Player {checkers[current_player]} won!")
            break
            
        if check_draw(board):
            print("The game is a draw!")
            break

        current_player = (current_player + 1) % num_players

# Start the game with predefined settings: 6 rows, 7 columns, 2 players
if __name__ == "__main__":
    play_game(ROWS, COLUMNS, PLAYERS)
