import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O']  # Adjust this list for more players if needed

# Initialize the board
def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

# Print the board
def print_board(board):
    os.system('clear')  # Clear the console
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))
    print("+" + "---+" * COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)

# Check for a win
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
    
    # Check diagonal (bottom-left to top-right)
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if all(board[r + i][c + i] == player for i in range(4)):
                return True
    
    # Check diagonal (top-left to bottom-right)
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if all(board[r - i][c + i] == player for i in range(4)):
                return True
                
    return False

# Check for a draw
def check_draw(board):
    return all(board[0][c] != " " for c in range(COLS))

# Get column input from player
def get_column_input(player):
    valid_input = False
    while not valid_input:
        col_input = input(f"Player {player}, please enter a column (A-{chr(65 + COLS - 1)}): ").upper()
        if len(col_input) == 1 and 'A' <= col_input <= chr(65 + COLS - 1):
            col_index = ord(col_input) - 65
            return col_index
        else:
            print("Invalid input. Please try again.")

# Place a checker in the board
def place_checker(board, col_index, player):
    for r in range(ROWS - 1, -1, -1):
        if board[r][col_index] == " ":
            board[r][col_index] = player
            return True
    return False

# Main game loop
def main():
    board = create_board()
    current_player_index = random.randint(0, len(PLAYERS) - 1)
    print_board(board)

    while True:
        current_player = PLAYERS[current_player_index]
        col_index = get_column_input(current_player)
        
        if place_checker(board, col_index, current_player):
            print_board(board)

            if check_win(board, current_player):
                print(f"Player {current_player} won!")
                break
            
            if check_draw(board):
                print("The game is a draw!")
                break

            current_player_index = (current_player_index + 1) % len(PLAYERS)
        else:
            print("Column is full. Please try a different column.")

if __name__ == "__main__":
    main()
