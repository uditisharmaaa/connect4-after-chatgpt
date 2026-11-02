import os
import random

# Constants for the game
ROWS = 6
COLS = 7
MAX_COLS = 26
PLAYERS = ['X', 'O', 'V', 'H', 'M']

# Initialize the game board
def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

# Print the board
def print_board(board):
    os.system('clear')  # Clear the terminal screen
      
    # Print column headers
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))
    print("+" + "---+".join([""] * COLS) + "---+")
    
    # Print the board rows
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+".join([""] * COLS) + "---+")

# Check for valid column input
def is_valid_input(col):
    if col in range(COLS):
        return True
    return False

# Find the next available row in the specified column
def get_next_open_row(board, col):
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == " ":
            return r
    return None

# Check for a win in various directions
def check_win(board, player):
    # Check horizontal
    for r in range(ROWS):
        for c in range(COLS - 3):
            if all(board[r][c + i] == player for i in range(4)):
                return True
    
    # Check vertical
    for c in range(COLS):
        for r in range(ROWS - 3):
            if all(board[r + i][c] == player for i in range(4)):
                return True
    
    # Check diagonal (positive slope)
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if all(board[r + i][c + i] == player for i in range(4)):
                return True

    # Check diagonal (negative slope)
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if all(board[r - i][c + i] == player for i in range(4)):
                return True

    return False

# Check for a draw
def is_draw(board):
    return all(board[0][c] != " " for c in range(COLS))

# Main function to play the game
def play_game():
    board = create_board()
    game_over = False
    turn = random.randint(0, len(PLAYERS) - 1)
    
    while not game_over:
        print_board(board)
        current_player = PLAYERS[turn]
        col = -1
        
        # Player input with validation
        while True:
            try:
                column_input = input(f"Player {current_player}, please enter a column (A-{chr(65 + COLS - 1)}): ").upper()
                
                if not column_input.isalpha() or len(column_input) != 1:
                    raise ValueError
                col = ord(column_input) - 65
                
                if is_valid_input(col):
                    row = get_next_open_row(board, col)
                    if row is not None:
                        board[row][col] = current_player
                        break
                    else:
                        print("Column full. Please choose another column.")
                else:
                    print("Invalid column. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a column letter (A-G).")
        
        # Check for win
        if check_win(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            game_over = True
        
        # Check for draw
        elif is_draw(board):
            print_board(board)
            print("It's a draw!")
            game_over = True
        
        # Switch turn to the next player
        turn = (turn + 1) % len(PLAYERS)

# Start the game
if __name__ == "__main__":
    play_game()
