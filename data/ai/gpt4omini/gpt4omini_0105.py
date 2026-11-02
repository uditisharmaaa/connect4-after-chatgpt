import os
import random

# Constants for board dimensions and players
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O']  # You can change this for more players

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')  # Clear the terminal
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))  # Column labels A, B, C, ...
    print("+---" + "---+" * (COLS - 1) + "---+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" + "---+" * (COLS - 1) + "---+")

def is_valid_input(column):
    return column.isalpha() and len(column) == 1 and 'A' <= column <= chr(65 + COLS - 1)

def find_empty_row(board, column):
    for row in range(ROWS - 1, -1, -1):  # Start from the bottom
        if board[row][column] == ' ':
            return row
    return -1  # Column is full

def check_winner(board, player):
    # Check horizontal, vertical, and diagonal win
    for row in range(ROWS):
        for col in range(COLS):
            if (col + 3 < COLS and all(board[row][col + i] == player for i in range(4))) or \
               (row + 3 < ROWS and all(board[row + i][col] == player for i in range(4))) or \
               (col + 3 < COLS and row + 3 < ROWS and all(board[row + i][col + i] == player for i in range(4))) or \
               (col - 3 >= 0 and row + 3 < ROWS and all(board[row + i][col - i] == player for i in range(4))):
                return True
    return False

def is_draw(board):
    return all(board[0][col] != ' ' for col in range(COLS))

def main():
    board = create_board()
    current_player_index = random.randint(0, len(PLAYERS) - 1)
    
    while True:
        print_board(board)
        current_player = PLAYERS[current_player_index]
        print(f"Player {current_player}, please enter a column (A-{chr(65 + COLS - 1)}):")
        
        column_input = input().upper()
        if not is_valid_input(column_input):
            print("Invalid input. Please try again.")
            continue
        
        column = ord(column_input) - 65  # Convert letter to column index
        row = find_empty_row(board, column)
        if row == -1:
            print("Column is full. Please choose another column.")
            continue
        
        board[row][column] = current_player
        
        if check_winner(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break
        
        if is_draw(board):
            print_board(board)
            print("The game is a draw!")
            break
        
        current_player_index = (current_player_index + 1) % len(PLAYERS)  # Switch to the next player

if __name__ == "__main__":
    main()
