import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O', 'V', 'H', 'M']

# Initialize the board
def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

# Print the board
def print_board(board):
    os.system('clear')
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))
    print("+" + "---+" * COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)

# Place a checker in the board
def place_checker(board, column, checker):
    for row in reversed(board):
        if row[column] == ' ':
            row[column] = checker
            return True
    return False

# Check for a win
def check_win(board, checker):
    # Check horizontal, vertical, and diagonal
    for r in range(ROWS):
        for c in range(COLS):
            if (c <= COLS - 4 and all(board[r][c+i] == checker for i in range(4)) or
                r <= ROWS - 4 and all(board[r+i][c] == checker for i in range(4)) or
                r <= ROWS - 4 and c <= COLS - 4 and all(board[r+i][c+i] == checker for i in range(4)) or
                r >= 3 and c <= COLS - 4 and all(board[r-i][c+i] == checker for i in range(4))):
                return True
    return False

# Check for a draw
def check_draw(board):
    return all(cell != ' ' for row in board for cell in row)

# Main function to run the game
def main():
    board = create_board()
    current_player = random.choice(PLAYERS)
    
    print_board(board)
    
    while True:
        col_input = input(f"Player {current_player}, please enter a column (A-{chr(65 + COLS - 1)}): ").upper()
        if not (col_input.isalpha() and ord(col_input) - 65 < COLS):
            print("Invalid input. Please try again.")
            continue
        
        column_index = ord(col_input) - 65
        
        if place_checker(board, column_index, current_player):
            print_board(board)
            if check_win(board, current_player):
                print(f"Player {current_player} won!")
                break
            if check_draw(board):
                print("The game is a draw!")
                break
            
            current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % len(PLAYERS)]
        else:
            print("Column full. Please choose another column.")

if __name__ == "__main__":
    main()
