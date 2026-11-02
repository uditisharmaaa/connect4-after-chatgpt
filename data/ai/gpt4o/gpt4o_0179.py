import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]  # Checkers for max 5 players

def clear_screen():
    os.system('clear')

def initialize_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    print("  " + "   ".join(chr(65+i) for i in range(len(board[0]))))
    print("+" + "---+" * len(board[0]))
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * len(board[0]))

def validate_input(input_str, board):
    if len(input_str) != 1 or not input_str.isalpha():
        return False
    column = ord(input_str.upper()) - 65
    if column < 0 or column >= len(board[0]):
        return False
    if board[0][column] != " ":
        return False
    return True

def place_checker(board, column, checker):
    for i in reversed(range(len(board))):
        if board[i][column] == " ":
            board[i][column] = checker
            return

def check_winner(board, checker):
    # Check horizontally
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True

    # Check vertically
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == checker for i in range(4)):
                return True
    
    # Check diagonally (down-right)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True

    # Check diagonally (down-left)
    for row in range(ROWS - 3):
        for col in range(3, COLUMNS):
            if all(board[row + i][col - i] == checker for i in range(4)):
                return True
    
    return False

def check_draw(board):
    return all(cell != " " for row in board for cell in row)

def play_game():
    # Initialize the game board
    board = initialize_board(ROWS, COLUMNS)

    # Randomly select a starting player
    current_player = random.randint(0, PLAYERS - 1)
    
    while True:
        print_board(board)
        print(f"Player {CHECKERS[current_player]}, please enter a column:")
        player_input = input().strip()
        
        while not validate_input(player_input, board):
            print("Invalid input. Please enter a valid column:")
            player_input = input().strip()
        
        column = ord(player_input.upper()) - 65
        place_checker(board, column, CHECKERS[current_player])
        
        if check_winner(board, CHECKERS[current_player]):
            print_board(board)
            print(f"Player {CHECKERS[current_player]} won!")
            break
        
        if check_draw(board):
            print_board(board)
            print("It's a draw!")
            break
        
        # Switch to the next player
        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    play_game()
