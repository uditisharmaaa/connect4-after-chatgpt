import os
import sys
import random

# Constants for game configuration
NUM_ROWS = 6
NUM_COLUMNS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]  # for up to 5 players

def clear_screen():
    # Clear the console screen
    os.system('clear')

def print_board(board):
    # Print the game board
    print("  " + "   ".join(chr(65 + i) for i in range(NUM_COLUMNS)))
    print("+---" * NUM_COLUMNS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * NUM_COLUMNS + "+")

def initialize_board():
    # Initialize the board with spaces
    return [[" " for _ in range(NUM_COLUMNS)] for _ in range(NUM_ROWS)]

def get_valid_input():
    # Get valid column input from the player
    while True:
        column_input = input("Please enter a column: ").upper()
        if len(column_input) == 1 and column_input.isalpha():
            column_index = ord(column_input) - 65
            if 0 <= column_index < NUM_COLUMNS:
                return column_index
        print("Invalid input. Please enter a valid column.")

def place_checker(board, column, checker):
    # Place the checker in the lowest available row in the specified column
    for row in reversed(range(NUM_ROWS)):
        if board[row][column] == " ":
            board[row][column] = checker
            return True
    return False

def check_for_win(board, checker):
    # Check for any win condition (horizontal, vertical, diagonal)
    def check_direction(x, y, dx, dy):
        count = 0
        for step in range(4):
            if (0 <= x + step*dx < NUM_ROWS) and (0 <= y + step*dy < NUM_COLUMNS):
                if board[x + step*dx][y + step*dy] == checker:
                    count += 1
                else:
                    break
        return count == 4
    
    for x in range(NUM_ROWS):
        for y in range(NUM_COLUMNS):
            if board[x][y] == checker:
                # Check horizontal, vertical, and two diagonal directions
                if (check_direction(x, y, 0, 1) or
                    check_direction(x, y, 1, 0) or
                    check_direction(x, y, 1, 1) or
                    check_direction(x, y, 1, -1)):
                    return True
    return False

def check_for_draw(board):
    # Check if the board is full
    for row in board:
        if " " in row:
            return False
    return True

def main():
    # Main function for running the game
    board = initialize_board()
    current_player = random.randint(0, NUM_PLAYERS - 1)  # Choose random starting player
    clear_screen()
    print_board(board)
    
    while True:
        print(f"Player {CHECKERS[current_player]}")
        column = get_valid_input()
        
        if place_checker(board, column, CHECKERS[current_player]):
            clear_screen()
            print_board(board)
            
            if check_for_win(board, CHECKERS[current_player]):
                print(f"Player {CHECKERS[current_player]} won!")
                break
            elif check_for_draw(board):
                print("The game is a draw!")
                break
            
            # Alternate current player
            current_player = (current_player + 1) % NUM_PLAYERS
        else:
            print("Column is full. Try a different column.")

if __name__ == "__main__":
    main()
