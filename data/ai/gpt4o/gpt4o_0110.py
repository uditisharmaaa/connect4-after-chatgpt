import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
WIN_LENGTH = 4

# Initialize the game
def initialize_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def display_board(board):
    os.system('clear')  # Use 'clear' for Unix/Linux Terminal
    print("  " + "   ".join(chr(ord('A') + i) for i in range(COLUMNS)))
    print("+---" * COLUMNS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

def get_next_open_row(board, column):
    for r in range(ROWS - 1, -1, -1):
        if board[r][column] == " ":
            return r
    return None

def drop_checker(board, row, column, checker):
    board[row][column] = checker

def is_valid_location(board, column):
    return board[0][column] == " "

def winning_move(board, checker):
    # Check horizontal locations for win
    for r in range(ROWS):
        for c in range(COLUMNS - WIN_LENGTH + 1):
            if all(board[r][c + i] == checker for i in range(WIN_LENGTH)):
                return True
                
    # Check vertical locations for win
    for c in range(COLUMNS):
        for r in range(ROWS - WIN_LENGTH + 1):
            if all(board[r + i][c] == checker for i in range(WIN_LENGTH)):
                return True
                
    # Check positively sloped diagonals
    for r in range(ROWS - WIN_LENGTH + 1):
        for c in range(COLUMNS - WIN_LENGTH + 1):
            if all(board[r + i][c + i] == checker for i in range(WIN_LENGTH)):
                return True
                
    # Check negatively sloped diagonals
    for r in range(WIN_LENGTH - 1, ROWS):
        for c in range(COLUMNS - WIN_LENGTH + 1):
            if all(board[r - i][c + i] == checker for i in range(WIN_LENGTH)):
                return True
                
    return False

def is_draw(board):
    return all(board[0][c] != " " for c in range(COLUMNS))

def main():
    # Initialize variables
    board = initialize_board()
    num_players = 2  # Set to 2 players, constant as per submission request
    player_checkers = ["X", "O", "V", "H", "M"][:num_players]
    
    current_player = random.choice(range(num_players))
    
    game_over = False

    while not game_over:
        display_board(board)
        print(f"Player {player_checkers[current_player]}, please enter a column:")
        
        # Input validation
        while True:
            try:
                column_input = input().strip().upper()
                if column_input.isalpha() and len(column_input) == 1:
                    column = ord(column_input) - ord('A')
                    if 0 <= column < COLUMNS and is_valid_location(board, column):
                        break
            except ValueError:
                pass
            print("Invalid input. Please enter a valid column.")

        row = get_next_open_row(board, column)
        if row is not None:
            drop_checker(board, row, column, player_checkers[current_player])
            
            # Winning move check
            if winning_move(board, player_checkers[current_player]):
                display_board(board)
                print(f"Player {player_checkers[current_player]} won!")
                game_over = True

            # Draw check
            elif is_draw(board):
                display_board(board)
                print("The game is a draw!")
                game_over = True

            # Alternate player
            current_player = (current_player + 1) % num_players

if __name__ == '__main__':
    main()
