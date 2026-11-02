import os
import random

# Constants for the game
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O', 'V', 'H', 'M']  # List of player checkers, can support up to 5 players

def initialize_board():
    # Create a 2D board initialized with whitespaces
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    # Clear the console
    os.system('clear')
    
    # Print column labels
    print("  " + '   '.join(chr(65 + i) for i in range(COLS)))
    print('+' + '---+' * COLS)

    # Print the board rows
    for row in board:
        print('|' + '|'.join(' ' + cell + ' ' for cell in row) + '|')
        print('+' + '---+' * COLS)

def is_valid_column(col):
    # Check if the column input is valid (A-G or a valid range)
    return col.isalpha() and 0 <= ord(col.upper()) - 65 < COLS

def get_column_index(col):
    # Convert the column letter (A-G) to an index (0-6)
    return ord(col.upper()) - 65

def is_column_full(board, col):
    # Check if the provided column is full
    return board[0][col] != ' '

def place_checker(board, col, checker):
    # Place the checker in the column if there is space
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = checker
            return True
    return False

def check_win(board, checker):
    # Check for horizontal, vertical, and diagonal wins
    def check_direction(delta_row, delta_col):
        count = 0
        for row in range(ROWS):
            for col in range(COLS):
                if board[row][col] == checker:
                    count = 1
                    r, c = row + delta_row, col + delta_col
                    while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
                        count += 1
                        if count == 4:
                            return True
                        r += delta_row
                        c += delta_col
                count = 0
        return False

    # Check in all four directions
    return (check_direction(0, 1) or  # Horizontal
            check_direction(1, 0) or  # Vertical
            check_direction(1, 1) or  # Diagonal down-right
            check_direction(1, -1))   # Diagonal down-left

def check_draw(board):
    # Check if the board is full (draw condition)
    return all(board[0][col] != ' ' for col in range(COLS))

def play_game():
    # Initialize game board and select first player
    board = initialize_board()
    current_player_index = random.randint(0, len(PLAYERS) - 1)

    while True:
        print_board(board)
        current_checker = PLAYERS[current_player_index]
        print(f"Player {current_checker}, please enter a column:")

        while True:
            column = input().strip()
            if not is_valid_column(column):
                print("Invalid input. Please enter a letter (A-G).")
                continue

            col_index = get_column_index(column)

            if is_column_full(board, col_index):
                print("Column is full! Choose another column.")
            else:
                place_checker(board, col_index, current_checker)
                break  # Exit loop upon successful placement

        if check_win(board, current_checker):
            print_board(board)
            print(f"Player {current_checker} won!")
            break
        
        if check_draw(board):
            print_board(board)
            print("It's a draw!")
            break
        
        # Switch to the next player
        current_player_index = (current_player_index + 1) % len(PLAYERS)

# Main function to run the game
if __name__ == "__main__":
    play_game()
