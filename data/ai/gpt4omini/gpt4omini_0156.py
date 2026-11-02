import os
import random

ROWS = 6
COLS = 7
PLAYERS = ['X', 'O']  # You can modify this to ['X', 'O', 'V', 'H', 'M'] for more players

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')  # Use 'cls' for Windows
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))
    print("+" + "---+" * COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)

def is_valid_input(column):
    return column.isalpha() and len(column) == 1 and 'A' <= column <= chr(65 + COLS - 1)

def get_column_index(column):
    return ord(column) - 65

def drop_checker(board, column, checker):
    for row in reversed(board):  # Start from the bottom row
        if row[get_column_index(column)] == ' ':
            row[get_column_index(column)] = checker
            return True
    return False

def check_winner(board, checker):
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True

    # Check vertical
    for col in range(COLS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == checker for i in range(4)):
                return True

    # Check diagonal (top-left to bottom-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True

    # Check diagonal (bottom-left to top-right)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True

    return False

def is_draw(board):
    return all(cell != ' ' for row in board for cell in row)

def main():
    board = create_board()
    current_player_index = random.randint(0, len(PLAYERS) - 1)
    
    while True:
        print_board(board)
        current_player = PLAYERS[current_player_index]
        
        while True:
            column = input(f"Player {current_player}, please enter a column (A-G): ").upper()
            if is_valid_input(column) and drop_checker(board, column, current_player):
                break
            print("Invalid input or column is full. Please try again.")

        if check_winner(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break
        
        if is_draw(board):
            print_board(board)
            print("The game is a draw!")
            break

        current_player_index = (current_player_index + 1) % len(PLAYERS)

if __name__ == "__main__":
    main()
