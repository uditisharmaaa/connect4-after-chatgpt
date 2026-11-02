import random
import os

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]

def clear_screen():
    os.system('clear')

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    print("  " + "   ".join(chr(65+i) for i in range(COLS)))
    print("+---" * COLS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLS + "+")

def get_valid_column(board):
    while True:
        col_input = input("Please enter a column: ").upper()
        if col_input.isalpha() and len(col_input) == 1:
            col = ord(col_input) - 65
            if 0 <= col < COLS and board[0][col] == ' ':
                return col
        print("Invalid input, try again.")

def place_checker(board, col, checker):
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = checker
            break

def check_winner(board, checker):
    # Horizontal
    for y in range(ROWS):
        for x in range(COLS-3):
            if all(board[y][x+i] == checker for i in range(4)):
                return True
    # Vertical
    for x in range(COLS):
        for y in range(ROWS-3):
            if all(board[y+i][x] == checker for i in range(4)):
                return True
    # Diagonal /
    for x in range(COLS-3):
        for y in range(3, ROWS):
            if all(board[y-i][x+i] == checker for i in range(4)):
                return True
    # Diagonal \
    for x in range(COLS-3):
        for y in range(ROWS-3):
            if all(board[y+i][x+i] == checker for i in range(4)):
                return True
    return False

def check_draw(board):
    return all(cell != ' ' for row in board for cell in row)

def main():
    board = create_board()
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    while True:
        print_board(board)
        print(f"Player {CHECKERS[current_player_index]}'s turn.")
        col = get_valid_column(board)
        place_checker(board, col, CHECKERS[current_player_index])
        
        if check_winner(board, CHECKERS[current_player_index]):
            print_board(board)
            print(f"Player {CHECKERS[current_player_index]} won!")
            break
        
        if check_draw(board):
            print_board(board)
            print("It's a draw!")
            break
        
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
