import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
PLAYERS = ["X", "O", "V", "H", "M"]
EMPTY_CELL = " "

# Initialize the board
def create_board():
    return [[EMPTY_CELL for _ in range(COLUMNS)] for _ in range(ROWS)]

# Print the board
def print_board(board):
    os.system('clear')  # Clear the screen
    print("  " + "   ".join(chr(65 + i) for i in range(COLUMNS)))
    print("+---" * COLUMNS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")
    print()

# Check if a column is valid
def is_valid_column(column, board):
    return column.isalpha() and len(column) == 1 and 'A' <= column < chr(65 + COLUMNS)

# Place a checker in the board
def place_checker(column, player, board):
    col_index = ord(column) - 65
    for row in reversed(range(ROWS)):
        if board[row][col_index] == EMPTY_CELL:
            board[row][col_index] = player
            return True
    return False

# Check for a win
def check_win(board, player):
    def check_direction(start_row, start_col, delta_row, delta_col):
        count = 0
        row, col = start_row, start_col
        while 0 <= row < ROWS and 0 <= col < COLUMNS and board[row][col] == player:
            count += 1
            row += delta_row
            col += delta_col
        return count

    for r in range(ROWS):
        for c in range(COLUMNS):
            if board[r][c] == player:
                if (check_direction(r, c, 0, 1) >= 4 or  # Horizontal
                    check_direction(r, c, 1, 0) >= 4 or  # Vertical
                    check_direction(r, c, 1, 1) >= 4 or  # Diagonal down-right
                    check_direction(r, c, 1, -1) >= 4):  # Diagonal down-left
                    return True
    return False

# Check for a draw
def check_draw(board):
    return all(board[0][col] != EMPTY_CELL for col in range(COLUMNS))

# Main function to play the game
def play_game():
    board = create_board()
    players = PLAYERS[:2]  # Set number of players to 2 as per the instructions
    current_player = random.choice(players)
    
    print_board(board)
    print(f"Player {current_player} goes first!")

    while True:
        print_board(board)
        column = input(f"Player {current_player}, please enter a column: ").strip().upper()
        
        # Validate input
        if not is_valid_column(column, board):
            print("Invalid input. Please enter a valid column letter (e.g., A-G).")
            continue
        
        col_index = ord(column) - 65
        
        # Check if column is full
        if board[0][col_index] != EMPTY_CELL:
            print("This column is full. Please choose another.")
            continue
        
        # Place checker
        place_checker(column, current_player, board)
        
        # Check for win
        if check_win(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break
        
        # Check for draw
        if check_draw(board):
            print_board(board)
            print("It's a draw!")
            break
        
        # Switch players
        current_player = players[(players.index(current_player) + 1) % len(players)]

# Run the game
if __name__ == "__main__":
    play_game()
