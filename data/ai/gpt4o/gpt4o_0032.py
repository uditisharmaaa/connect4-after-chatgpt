import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2  # can be set to 3, 4, or 5
CHECKERS = ['X', 'O', 'V', 'H', 'M']  # available checkers

# Function to clear the screen
def clear_screen():
    os.system('clear')

# Initialize the board
def create_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

# Print the board
def print_board(board):
    clear_screen()
    print("  " + "   ".join(chr(65 + i) for i in range(COLUMNS)))
    print("+" + "---+" * COLUMNS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLUMNS)

# Check if a move is valid
def is_valid_move(board, column):
    return board[0][column] == " "

# Place a checker on the board
def place_checker(board, column, checker):
    for row in range(ROWS - 1, -1, -1):
        if board[row][column] == " ":
            board[row][column] = checker
            break

# Check for win conditions
def check_win(board, checker):
    # Check horizontal, vertical and diagonal
    for r in range(ROWS):
        for c in range(COLUMNS):
            if (c + 3 < COLUMNS and all(board[r][c + i] == checker for i in range(4))) or \
               (r + 3 < ROWS and all(board[r + i][c] == checker for i in range(4))) or \
               (r + 3 < ROWS and c + 3 < COLUMNS and all(board[r + i][c + i] == checker for i in range(4))) or \
               (r - 3 >= 0 and c + 3 < COLUMNS and all(board[r - i][c + i] == checker for i in range(4))):
                return True
    return False

# Check if the board is full for a draw
def is_draw(board):
    return all(board[0][c] != " " for c in range(COLUMNS))

# Main game function
def play_game():
    board = create_board()
    players = CHECKERS[:PLAYERS]
    current_player_idx = random.randint(0, PLAYERS - 1)
    print_board(board)

    while True:
        current_player = players[current_player_idx]
        move = None
        while move is None:
            col_input = input(f"Player {current_player}, please enter a column: ").strip().upper()
            if len(col_input) == 1 and 'A' <= col_input <= chr(65 + COLUMNS - 1):
                column = ord(col_input) - 65
                if is_valid_move(board, column):
                    move = column
                else:
                    print("Invalid move, column is full.")
            else:
                print("Invalid input, please enter a valid column letter.")
        
        place_checker(board, move, current_player)
        print_board(board)
        
        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            break
        if is_draw(board):
            print("The game is a draw!")
            break
        
        current_player_idx = (current_player_idx + 1) % PLAYERS

# Start the game
if __name__ == "__main__":
    play_game()
