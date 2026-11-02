import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = ["X", "O", "V", "H", "M"]  # Up to 5 players

def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')  # Use 'cls' on Windows
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))  # Column headers A-G
    print("+" + "---+" * COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)

def is_valid_input(column_input):
    if len(column_input) != 1 or not column_input.isalpha():
        return False
    column_index = ord(column_input.upper()) - 65
    return 0 <= column_index < COLS

def get_column_index(column_input):
    return ord(column_input.upper()) - 65

def drop_checker(board, column_index, checker):
    for row in reversed(board):
        if row[column_index] == " ":
            row[column_index] = checker
            return True
    return False

def check_winner(board, checker):
    # Check horizontal, vertical, and diagonal for win
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == checker:
                # Check horizontal
                if col + 3 < COLS and all(board[row][col + i] == checker for i in range(4)):
                    return True
                # Check vertical
                if row + 3 < ROWS and all(board[row + i][col] == checker for i in range(4)):
                    return True
                # Check diagonal (positive slope)
                if row + 3 < ROWS and col + 3 < COLS and all(board[row + i][col + i] == checker for i in range(4)):
                    return True
                # Check diagonal (negative slope)
                if row - 3 >= 0 and col + 3 < COLS and all(board[row - i][col + i] == checker for i in range(4)):
                    return True
    return False

def is_draw(board):
    return all(cell != " " for row in board for cell in row)

def main():
    board = create_board()
    current_player_index = random.randint(0, len(PLAYERS) - 1)
    
    print_board(board)
    
    while True:
        current_checker = PLAYERS[current_player_index]
        column_input = input(f"Player {current_checker}, please enter a column: ").strip().upper()
        
        if not is_valid_input(column_input):
            print("Invalid input. Please enter a letter from A to G.")
            continue
        
        column_index = get_column_index(column_input)
        
        if not drop_checker(board, column_index, current_checker):
            print("Column is full. Please choose another column.")
            continue
        
        print_board(board)
        
        if check_winner(board, current_checker):
            print(f"Player {current_checker} won!")
            break
        
        if is_draw(board):
            print("The game is a draw!")
            break
        
        current_player_index = (current_player_index + 1) % len(PLAYERS)

if __name__ == "__main__":
    main()
