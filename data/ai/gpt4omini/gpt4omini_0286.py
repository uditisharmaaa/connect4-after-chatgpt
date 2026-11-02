import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = ["X", "O", "V", "H", "M"]

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))
    print("+---" * COLS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLS + "+")

def is_valid_input(col):
    return col.isalpha() and len(col) == 1 and 'A' <= col <= chr(65 + COLS - 1)

def get_column_index(col):
    return ord(col) - 65

def place_checker(board, col, player):
    for row in reversed(board):
        if row[get_column_index(col)] == ' ':
            row[get_column_index(col)] = player
            return True
    return False

def check_win(board, player):
    # Check horizontal
    for row in board:
        for col in range(COLS - 3):
            if all(cell == player for cell in row[col:col + 4]):
                return True
    # Check vertical
    for col in range(COLS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == player for i in range(4)):
                return True
    # Check diagonal (bottom-left to top-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == player for i in range(4)):
                return True
    # Check diagonal (top-left to bottom-right)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i][col + i] == player for i in range(4)):
                return True
    return False

def check_draw(board):
    return all(cell != ' ' for row in board for cell in row)

def main():
    board = create_board()
    current_player_index = random.randint(0, min(len(PLAYERS) - 1, 1))
    
    print_board(board)
    
    while True:
        current_player = PLAYERS[current_player_index]
        col = input(f"Player {current_player}, please enter a column: ").upper()
        
        while not is_valid_input(col) or not place_checker(board, col, current_player):
            print("Invalid input. Please try again.")
            col = input(f"Player {current_player}, please enter a column: ").upper()
        
        print_board(board)
        
        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            break
        
        if check_draw(board):
            print("The game is a draw!")
            break
        
        current_player_index = (current_player_index + 1) % len(PLAYERS)

if __name__ == "__main__":
    main()
