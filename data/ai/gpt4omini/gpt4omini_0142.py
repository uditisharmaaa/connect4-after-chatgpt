import os
import random

# Constants for the game dimensions and players
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O']  # You can add more players if necessary

# Function to create the Connect 4 board
def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

# Function to print the board
def print_board(board):
    os.system('clear')  # Clear the terminal screen
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))  # Column labels A-G
    print("+" + "---+" * COLS)
    
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)

# Function to check for a win
def check_win(board, player):
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col + i] == player for i in range(4)):
                return True

    # Check vertical
    for col in range(COLS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == player for i in range(4)):
                return True
                
    # Check diagonal (down-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == player for i in range(4)):
                return True
                
    # Check diagonal (down-left)
    for row in range(ROWS - 3):
        for col in range(3, COLS):
            if all(board[row + i][col - i] == player for i in range(4)):
                return True

    return False

# Function to check for a draw
def check_draw(board):
    return all(board[0][col] != ' ' for col in range(COLS))

# Function to drop a checker in the column
def drop_checker(board, col, player):
    for row in reversed(range(ROWS)):
        if board[row][col] == ' ':
            board[row][col] = player
            return True
    return False  # Column is full

def main():
    # Initialize game
    board = create_board()
    current_player_index = random.randint(0, len(PLAYERS) - 1)

    print_board(board)

    while True:
        current_player = PLAYERS[current_player_index]
        valid_input = False

        while not valid_input:
            column_input = input(f"Player {current_player}, please enter a column (A-G): ").upper()
            if column_input in 'ABCDEFG' and drop_checker(board, ord(column_input) - 65, current_player):
                valid_input = True
            else:
                print("Invalid input. Please try again.")

        print_board(board)

        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            break

        if check_draw(board):
            print("The game is a draw!")
            break
        
        # Switch players
        current_player_index = (current_player_index + 1) % len(PLAYERS)

if __name__ == '__main__':
    main()
