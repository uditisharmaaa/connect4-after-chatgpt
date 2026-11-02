import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')  # Clear the screen
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))
    print("+" + "---+" * COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)

def get_available_row(board, col):
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            return row
    return -1

def is_valid_input(col):
    return col.isalpha() and 'A' <= col.upper() <= chr(65 + COLS - 1)

def place_checker(board, col, checker):
    col_index = ord(col.upper()) - 65
    row_index = get_available_row(board, col_index)
    if row_index != -1:
        board[row_index][col_index] = checker
        return True
    return False

def check_win(board, checker):
    # Check horizontal win
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True
    
    # Check vertical win
    for col in range(COLS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == checker for i in range(4)):
                return True

    # Check diagonal (down/right) win
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True

    # Check diagonal (down/left) win
    for row in range(ROWS - 3):
        for col in range(3, COLS):
            if all(board[row + i][col - i] == checker for i in range(4)):
                return True

    return False

def is_draw(board):
    return all(board[0][col] != ' ' for col in range(COLS))

def main():
    board = create_board()
    current_player = random.randint(0, len(PLAYERS) - 1)
    print("Current Board:")
    print_board(board)
    
    while True:
        player_checker = PLAYERS[current_player]
        col = input(f"Player {player_checker}, please enter a column: ")
        
        while not is_valid_input(col) or not place_checker(board, col, player_checker):
            print("Invalid input or column is full! Try again.")
            col = input(f"Player {player_checker}, please enter a column: ")
        
        print_board(board)
        
        if check_win(board, player_checker):
            print(f"Player {player_checker} won!")
            break
        
        if is_draw(board):
            print("The game is a draw!")
            break
        
        current_player = (current_player + 1) % len(PLAYERS)

if __name__ == '__main__':
    main()
